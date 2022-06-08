from django.contrib import admin

from poll.models import Candidate, Ballot, CandidateBallot, User


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


@admin.register(CandidateBallot)
class CandidateBallotAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'washington',
        'adams',
        'jefferson',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'id',
        'washington',
        'adams',
        'jefferson',
    )
    date_hierarchy = 'created_at'
