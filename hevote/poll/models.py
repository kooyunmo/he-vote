from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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


class GenderCandidate(TimestampMixin):
    male_washington = models.BigIntegerField()
    female_washington = models.BigIntegerField()
    male_adams = models.BigIntegerField()
    female_adams = models.BigIntegerField()
    male_jefferson = models.BigIntegerField()
    female_jefferson = models.BigIntegerField()


class User(AbstractUser):
    class Gender(models.TextChoices):
        male = 'male', _('male')
        female = 'female', _('female')

    gender = models.CharField(choices=Gender.choices, max_length=24)
