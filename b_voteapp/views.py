from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required

from . models import Candidate, Vote, Election, Voter, Block

from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from django.db.models import Count


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
    candidates = Candidate.objects.filter(election=election).annotate(vote_count=Count('vote')).order_by('-vote_count', 'name')

    if election.end_time and election.end_time < timezone.now():
        status = 'Ended'
    elif election.is_active:
        status = 'Active'
    else:
        status = 'Inactive'


    can_vote = (
    status == 'Active' and
    request.user.college == election.college and
    (
        (election.election_type == 'Student Election' and request.user.is_student) or
        (election.election_type == 'Staff Election' and request.user.is_staff)
    )   
    )   

    # Tie-aware ranking
    ranking = {}
    current_rank = 0
    previous_votes = None
    position_count = 0  # for actual 1st, 2nd, 3rd etc
    for candidate in candidates:
        position_count += 1
        if candidate.vote_count != previous_votes:
            current_rank = position_count
        previous_votes = candidate.vote_count

        if current_rank == 1:
            rank_label = '🥇 1st Place'
        elif current_rank == 2:
            rank_label = '🥈 2nd Place'
        elif current_rank == 3:
            rank_label = '🥉 3rd Place'
        else:
            rank_label = f'{current_rank}th Place'

        ranking[candidate.id] = rank_label

    context = {
    'election': election,
    'status': status,
    'candidates': candidates,
    'ranking': ranking,
    'can_vote': can_vote,
    }

    return render(request, 'b_voteapp/election_detail.html', context)


#---------------------------------------------------------------------------------------------------------
# VOTING VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def cast_vote(request, election_pk):
    voter = get_object_or_404(Voter, user=request.user)
    election = get_object_or_404(Election, pk=election_pk)

    # Prevent double voting in this election specifically
    if Vote.objects.filter(voter=voter, candidate__election=election).exists():
        messages.success(request, 'You have already voted in this election. Multiple voting not allowed.')
        return redirect('b_voteapp:home')

    if request.method == "POST":
        candidate_id = request.POST.get('candidate_id')
        if not candidate_id:
            return render(request, 'error.html', {'message': "Please select a candidate to vote."})

        try:
            candidate = Candidate.objects.get(id=candidate_id, election=election)
        except Candidate.DoesNotExist:
            return render(request, 'error.html', {'message': "Selected candidate does not exist for this election."})

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

        messages.success(request, 'Your Vote has successfully been cast and recorded in the blockchain')
        return redirect('b_voteapp:home')

    else:
        # Show only candidates in the current election
        candidates = Candidate.objects.filter(election=election)
        return render(request, 'b_voteapp/vote.html', {'candidates': candidates, 'election': election})

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
                'candidate_role': candidate.role if candidate else "Unknown",
                'candidate_party': candidate.party if candidate else "Unknown",
                'election_name': election.election_name if election else "Unknown",
                'election_type': election.election_type if election else "Unknown",
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

