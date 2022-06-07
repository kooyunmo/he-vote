from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.decorators import action

from poll.errors import NotAuthenticatedError, NotFoundError, ParseError
from poll.serializers import WritableBallotSerializer, BallotSerializer
from poll.models import Ballot, Candidate, GenderCandidate
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
    def create(self, request: Request):
        self.initialize(request)
        serializer = WritableBallotSerializer(data=request.data)
        if not serializer.is_valid():
            raise ParseError(repr(serializer.errors))

        candidate_id = serializer.validated_data['candidate_id']

        try:
            cand = Candidate.objects.get(pk=candidate_id)
        except Candidate.DoesNotExist as exc:
            raise NotFoundError(f"Candidate with ID {candidate_id} is not found.") from exc

        ballot = Ballot(
            candidate_id=candidate_id
        )
        ballot.save()

        # Add ballot to ASHE
        fields = [
            'male_washington',
            'female_washington',
            'male_adams',
            'female_adams',
            'male_jefferson',
            'female_jefferson',
        ]
        field_dict = {}
        for field in fields:
            if field == f'{request.user.gender}_{cand.name.lower()}':
                ciphertext = self.cipher.encrypt(request.user.id, 1, f'{field}_{ballot.id}'.encode())
                field_dict[field] = ciphertext
            else:
                null_ciphertext = self.cipher.encrypt(request.user.id, 0, f'{field}_{ballot.id}'.encode())
                field_dict[field] = null_ciphertext
        breakpoint()

        gender_cand = GenderCandidate(**field_dict)
        gender_cand.save()

        return Response(BallotSerializer(ballot).data, status=HTTP_201_CREATED)        


class TallyViewSet(viewsets.ViewSet):
    ...
