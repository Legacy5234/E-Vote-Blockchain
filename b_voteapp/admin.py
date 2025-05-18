from django.contrib import admin
from .models import Voter, Candidate, Vote, Election, Block

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('user', 'voter_id', 'is_verified')
    search_fields = ('user__username', 'voter_id')
    list_filter = ('is_verified',)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'party')
    search_fields = ('name', 'party')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'candidate', 'timestamp', 'transaction_hash')
    search_fields = ('voter__user__username', 'candidate__name')

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'is_active')
    actions = ['start_election', 'stop_election']

    def start_election(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected elections started.")
    start_election.short_description = "Start selected elections"

    def stop_election(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected elections stopped.")
    stop_election.short_description = "Stop selected elections"

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('index', 'timestamp', 'previous_hash', 'hash', 'nonce')
    readonly_fields = ('index', 'timestamp', 'votes', 'previous_hash', 'hash', 'nonce')






