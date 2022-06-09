from typing import Dict, Type, Union

from django.db.models import Sum
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from poll.cipher.ashe import ASHECipher
from poll.cipher.base import CipherBase
from poll.cipher.bfv import BFVCipher
from poll.cipher.paillier import PaillierCipher
from poll.errors import NotAuthenticatedError, NotFoundError, ParseError
from poll.models import Ballot, Candidate, ASHECandidateBallot, BFVCandidateBallot, PaillierCandidateBallot
from poll.serializers import TallySerializer, WritableBallotSerializer, BallotSerializer


class CryptoMixin(viewsets.ViewSet):
    def initialize(self, request: Request, cipher: str):
        if not request.user.is_authenticated:
            raise NotAuthenticatedError

        cipher_cls_map: Dict[str, Type[CipherBase]] = {
            'ashe': ASHECipher,
            'bfv': BFVCipher,
            'paillier': PaillierCipher,
        }
        cipher_ballot_map: Dict[str, Union[Type[ASHECandidateBallot],
                                           Type[BFVCandidateBallot],
                                           Type[PaillierCandidateBallot]]] = {
            'ashe': ASHECandidateBallot,
            'bfv': BFVCandidateBallot,
            'paillier': PaillierCandidateBallot,
        }

        try:
            self.cipher = cipher_cls_map[cipher]()
        except KeyError as exc:
            raise ParseError from exc

        try:
            self.ballot_class = cipher_ballot_map[cipher]
        except KeyError as exc:
            raise ParseError from exc


class CastViewSet(CryptoMixin):
    @extend_schema(
        request=WritableBallotSerializer,
        responses={200: BallotSerializer}
    )
    def create(self, request: Request) -> Response:
        serializer = WritableBallotSerializer(data=request.data)
        if not serializer.is_valid():
            raise ParseError(repr(serializer.errors))

        candidate_id = serializer.validated_data['candidate_id']
        cipher = serializer.validated_data['cipher']
        self.initialize(request, cipher)

        try:
            cand = Candidate.objects.get(pk=candidate_id)
        except Candidate.DoesNotExist as exc:
            raise NotFoundError(f"Candidate with ID {candidate_id} is not found.") from exc

        ballot = Ballot(candidate_id=candidate_id)
        ballot.save()

        # Add ballot to ASHE
        fields = [
            'washington',
            'adams',
            'jefferson',
        ]
        field_dict = {}
        for field in fields:
            if field == cand.name.lower():
                ciphertext = self.cipher.encrypt(
                    id_=ballot.id,
                    plaintext=1,
                    nonce=field.encode()
                )
                field_dict[field] = ciphertext
            else:
                null_ciphertext = self.cipher.encrypt(
                    id_=ballot.id,
                    plaintext=0,
                    nonce=field.encode()
                )
                field_dict[field] = null_ciphertext

        cand_ballot = self.ballot_class(**field_dict)
        cand_ballot.save()

        return Response(BallotSerializer(ballot).data, status=HTTP_201_CREATED)        


class TallyViewSet(CryptoMixin):
    @extend_schema(
        parameters=[
            OpenApiParameter(name='cipher', required=True, type=str)
        ],
        responses={200: TallySerializer}
    )
    def list(self, request: Request) -> Response:
        self.initialize(request, request.query_params['cipher'])
        cand_ballots = self.ballot_class.objects.all()
        ballots = Ballot.objects.all()
        start_id = ballots.first().id
        end_id = ballots.last().id

        washington_esum = None
        adams_esum = None
        jefferson_esum = None

        for i, ballot in enumerate(cand_ballots):
            if i == 0:
                washington_esum = ballot.washington
                adams_esum = ballot.adams
                jefferson_esum = ballot.jefferson
            else:
                washington_esum = washington_esum + ballot.washington
                adams_esum = adams_esum + ballot.adams
                jefferson_esum = jefferson_esum + ballot.jefferson

        # washington_esum = cand_ballots.aggregate(Sum('washington'))['washington__sum']
        # adams_esum = cand_ballots.aggregate(Sum('adams'))['adams__sum']
        # jefferson_esum = cand_ballots.aggregate(Sum('jefferson'))['jefferson__sum']

        washington_sum = self.cipher.decrypt_sum(
            start_id=start_id - 1,
            end_id=end_id,
            ciphertext=washington_esum,
            nonce='washington'.encode(),
        )
        adams_sum = self.cipher.decrypt_sum(
            start_id=start_id - 1,
            end_id=end_id,
            ciphertext=adams_esum,
            nonce='adams'.encode(),
        )
        jefferson_sum = self.cipher.decrypt_sum(
            start_id=start_id - 1,
            end_id=end_id,
            ciphertext=jefferson_esum,
            nonce='jefferson'.encode(),
        )
        resp_data = [
            {
                'candidate_id': 1,
                'votes': washington_sum
            },
            {
                'candidate_id': 2,
                'votes': adams_sum
            },
            {
                'candidate_id': 3,
                'votes': jefferson_sum
            }
        ]

        return Response(TallySerializer(resp_data, many=True).data)
