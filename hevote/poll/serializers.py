from rest_framework import serializers

from poll.models import Ballot


class WritableBallotSerializer(serializers.ModelSerializer):
    candidate_id = serializers.IntegerField()

    class Meta:
        model = Ballot
        fields = ['candidate_id',]


class BallotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ballot
        fields = ['candidate_id',]


class TallySerializer(serializers.Serializer):
    candidate_id = serializers.IntegerField()
    votes = serializers.IntegerField()
    latency = serializers.FloatField()
