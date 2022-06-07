from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from poll.models import Candidate, Ballot, GenderCandidate, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'gender')


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'party',
    )
    search_fields = ('name',)


@admin.register(Ballot)
class BallotAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'candidate',
        'created_at',
        'updated_at',
    )
    search_fields = ('candidate', 'created_at', 'updated_at',)
    date_hierarchy = 'created_at'


@admin.register(GenderCandidate)
class GenderCandidateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'male_washington',
        'female_washington',
        'male_adams',
        'female_adams',
        'male_jefferson',
        'female_jefferson',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'id',
        'male_washington',
        'female_washington',
        'male_adams',
        'female_adams',
        'male_jefferson',
        'female_jefferson',
    )
    date_hierarchy = 'created_at'
