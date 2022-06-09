from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from picklefield.fields import PickledObjectField


class TimestampMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Candidate(models.Model):
    name = models.CharField(max_length=128)
    party = models.CharField(max_length=128)


class Ballot(TimestampMixin):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)


class ASHECandidateBallot(TimestampMixin):
    washington = models.BigIntegerField()
    adams = models.BigIntegerField()
    jefferson = models.BigIntegerField()


class BFVCandidateBallot(TimestampMixin):
    washington = PickledObjectField()
    adams = PickledObjectField()
    jefferson = PickledObjectField()


class PaillierCandidateBallot(TimestampMixin):
    washington = PickledObjectField()
    adams = PickledObjectField()
    jefferson = PickledObjectField()


class User(AbstractUser):
    class Gender(models.TextChoices):
        male = 'male', _('male')
        female = 'female', _('female')

    gender = models.CharField(choices=Gender.choices, max_length=24)
