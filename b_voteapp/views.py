from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required

from a_userauthapp.models import Voter_User
from . models import Candidate, Vote, Election, Voter, Block


from django.utils import timezone
from django.contrib import messages
from datetime import datetime

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


#---------------------------------------------------------------------------------------------------------
# ELECTION DETAIL VIEW
#---------------------------------------------------------------------------------------------------------
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
        'status': status,
    }
    return render(request, 'b_voteapp/election_detail.html', context)



#---------------------------------------------------------------------------------------------------------
# VOTING VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def cast_vote(request):
    voter = get_object_or_404(Voter, user=request.user)

    # Prevent double voting
    if Vote.objects.filter(voter=voter).exists():
        messages.success(request, 'You have already voted. Multiple voting not allowed.')
        return redirect('b_voteapp:home')

    if request.method == "POST":
        candidate_id = request.POST.get('candidate_id')
        if not candidate_id:
            return render(request, 'error.html', {'message': "Please select a candidate to vote."})

        try:
            candidate = Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            return render(request, 'error.html', {'message': "Selected candidate does not exist."})

        # Create vote data
        vote_data = {
            'voter_id': voter.voter_id,
            'candidate_id': candidate.id,
            'timestamp': time.time()
        }

        # Get last block
        try:
            last_block = Block.objects.latest('index')
            previous_hash = last_block.hash
            index = last_block.index + 1
        except Block.DoesNotExist:
            previous_hash = '0'
            index = 0

        # Create new block instance (without hash yet)
        new_block = Block(
            index=index,
            timestamp=time.time(),
            votes=json.dumps([vote_data]),
            previous_hash=previous_hash,
            nonce=0
        )

        # Proof-of-Work
        difficulty = 4
        computed_hash = new_block.compute_hash()
        while not computed_hash.startswith('0' * difficulty):
            new_block.nonce += 1
            computed_hash = new_block.compute_hash()

        new_block.hash = computed_hash
        new_block.save()

        # Save vote record, linking to block's hash
        Vote.objects.create(
            voter=voter,
            candidate=candidate,
            transaction_hash=new_block.hash
        )

        return render(request, 'b_voteapp/success.html')

    else:
        candidates = Candidate.objects.all()
        return render(request, 'b_voteapp/vote.html', {'candidates': candidates})



#---------------------------------------------------------------------------------------------------------
# BLOCKCHAIN EXPLORER VIEW
#---------------------------------------------------------------------------------------------------------
def blockchain_explorer(request):
    blocks = Block.objects.all().order_by('index')

    previous_hash = "0"

    for block in blocks:
        # Parse votes JSON string
        parsed_votes = json.loads(block.votes)
        enriched_votes = []

        for vote_data in parsed_votes:
            try:
                voter = Voter.objects.get(voter_id=vote_data['voter_id'])
                candidate = Candidate.objects.get(id=vote_data['candidate_id'])
                election = candidate.election
            except (Voter.DoesNotExist, Candidate.DoesNotExist):
                voter = None
                candidate = None
                election = None

            enriched_votes.append({
                'voter_id': vote_data['voter_id'],
                'voter_username': voter.user.username if voter else "Unknown",
                'candidate_name': candidate.name if candidate else "Unknown",
                'candidate_party': candidate.party if candidate else "Unknown",
                'election_name': election.name if election else "Unknown",
                'timestamp': datetime.fromtimestamp(vote_data['timestamp'])  # convert to datetime object
            })

        block.parsed_votes = enriched_votes
        block.vote_count = len(parsed_votes)

        is_valid = (block.previous_hash == previous_hash and block.hash == block.compute_hash())
        block.is_valid = is_valid
        previous_hash = block.hash

        block.formatted_timestamp = datetime.fromtimestamp(block.timestamp)  # convert block timestamp too

    return render(request, 'b_voteapp/explorer.html', {
        'blocks': blocks
    })

