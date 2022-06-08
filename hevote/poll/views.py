from typing import Dict, Type

from django.db.models import Sum
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from poll.errors import NotAuthenticatedError, NotFoundError, ParseError
from poll.serializers import TallySerializer, WritableBallotSerializer, BallotSerializer
from poll.models import Ballot, Candidate, CandidateBallot
from poll.cipher.base import CipherBase
from poll.cipher.ashe import ASHECipher


class CastViewSet(viewsets.ViewSet):
    def initialize(self, request: Request):
        if not request.user.is_authenticated:
            raise NotAuthenticatedError

        self.cipher = ASHECipher()

    @extend_schema(
        request=WritableBallotSerializer,
        responses={200: BallotSerializer}
    )
    def create(self, request: Request) -> Response:
        self.initialize(request)
        serializer = WritableBallotSerializer(data=request.data)
        if not serializer.is_valid():
            raise ParseError(repr(serializer.errors))

        candidate_id = serializer.validated_data['candidate_id']

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

        cand_ballot = CandidateBallot(**field_dict)
        cand_ballot.save()

        return Response(BallotSerializer(ballot).data, status=HTTP_201_CREATED)        


class TallyViewSet(viewsets.ViewSet):
    def initialize(self, request: Request):
        if not request.user.is_authenticated:
            raise NotAuthenticatedError

        params = request.query_params
        cipher_cls_map: Dict[str, Type[CipherBase]] = {
            'ashe': ASHECipher,
            # TODO: Add other schemes
        }

        try:
            self.cipher = cipher_cls_map[params['cipher']]()
        except KeyError as exc:
            raise ParseError from exc

    @extend_schema(
        parameters=[
            OpenApiParameter(name='cipher', required=True, type=str)
        ],
        responses={200: TallySerializer}
    )
    def list(self, request: Request) -> Response:
        self.initialize(request)
        cand_ballots = CandidateBallot.objects.all()
        ballots = Ballot.objects.all()
        start_id = ballots.first().id
        end_id = ballots.last().id

        washington_esum = cand_ballots.aggregate(Sum('washington'))['washington__sum']
        adams_esum = cand_ballots.aggregate(Sum('adams'))['adams__sum']
        jefferson_esum = cand_ballots.aggregate(Sum('jefferson'))['jefferson__sum']

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
