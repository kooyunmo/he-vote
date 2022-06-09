from django.contrib import admin

from poll.models import Candidate, Ballot, ASHECandidateBallot, BFVCandidateBallot, PaillierCandidateBallot, User


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


@admin.register(ASHECandidateBallot)
class ASHECandidateBallotAdmin(admin.ModelAdmin):
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


@admin.register(BFVCandidateBallot)
class BFVCandidateBallotAdmin(admin.ModelAdmin):
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


@admin.register(PaillierCandidateBallot)
class PaillierCandidateBallotAdmin(admin.ModelAdmin):
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
