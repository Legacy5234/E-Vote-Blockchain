from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required

from . models import Voter, Candidate, Vote
from b_voteapp.models import Election

from . blockchain import Blockchain
from django.utils import timezone
from django.contrib import messages

import time 
import json


#---------------------------------------------------------------------------------------------------------
# HOMEPAGE VIEW
#---------------------------------------------------------------------------------------------------------
def homepage(request):
    elections = Election.objects.all()

    # Add status attribute to each election
    for election in elections:
        if election.end_time < timezone.now():
            election.status = 'Ended'
        elif election.is_active:
            election.status = 'Active'
        else:
            election.status = 'Inactive'

    context = {
        'elections': elections
    }
    return render(request, 'b_voteapp/homepage.html', context)

@login_required(login_url='a_userauthapp:login')
def election_detail(request, pk):
    election = get_object_or_404(Election, pk=pk)

    # Determine election status
    if election.end_time < timezone.now():
        status = 'Ended'
    elif election.is_active:
        status = 'Active'
    else:
        status = 'Inactive'

    context = {
        'election': election,
        'status': status
    }
    return render(request, 'b_voteapp/election_detail.html', context)




blockchain = Blockchain()

def cast_vote(request):
    if request.method == "POST":
        voter = Voter.objects.get(user=request.user)
        if Vote.objects.filter(voter=voter).exists():
            return render(request, 'error.html', {'message': "You have already voted."})

        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.get(id=candidate_id)

        # Save vote temporarily
        vote_data = {
            'voter_id': voter.voter_id,
            'candidate_id': candidate.id,
            'timestamp': time.time()
        }

        # Add vote to blockchain
        blockchain.add_block([vote_data])

        # Save vote with blockchain hash
        Vote.objects.create(
            voter=voter,
            candidate=candidate,
            transaction_hash=blockchain.chain[-1]['hash']
        )

        return render(request, 'b_voteapp/success.html')
    else:
        candidates = Candidate.objects.all()
        return render(request, 'b_voteapp/vote.html', {'candidates': candidates})
