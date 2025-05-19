from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from . forms import ElectionForm, CandidateForm
from b_voteapp.models import Election, Candidate


#---------------------------------------------------------------------------------------------------------
# ADMIN VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def admin_dashboard(request):
    return render(request, 'e_vote_blockchain/admin-page.html')


#---------------------------------------------------------------------------------------------------------
# CREATE ELECTION VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def create_election(request):
    if request.method == 'POST':
        form = ElectionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-dashboard')
    else:
        form = ElectionForm()
    return render(request, 'e_vote_blockchain/create_election.html', {'form': form})


#---------------------------------------------------------------------------------------------------------
# CREATE CANDIDATE VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def create_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate added successfully..')
            return redirect('create_candidate')
    else:
        form = CandidateForm()
    return render(request, 'e_vote_blockchain/create_candidate.html', {'form': form})


#---------------------------------------------------------------------------------------------------------
# EDIT ELECTION VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def edit_election(request, pk):
    election = get_object_or_404(Election, pk=pk)
    if request.method == 'POST':
        form = ElectionForm(request.POST, request.FILES, instance=election)
        if form.is_valid():
            form.save()
            messages.success(request, 'Election Edited Successfully..')
            return redirect('b_voteapp:home')
    else:
        form = ElectionForm(instance=election)

    context = {
        'form':form,
        'election':election
    }
    return render(request, 'e_vote_blockchain/edit_election.html', context)

#---------------------------------------------------------------------------------------------------------
# DELETE ELECTION VIEW
#---------------------------------------------------------------------------------------------------------
def delete_election(request, pk):
    election = get_object_or_404(Election, pk=pk)
    if request.method == 'POST':
        election.delete()
        messages.success(request, 'Election Deleted Successfully..')
        return redirect('b_voteapp:home')
    return render(request, 'e_vote_blockchain/delete_election.html', {'election': election})



#---------------------------------------------------------------------------------------------------------
# EDIT CANDIDATE VIEW VIEW
#---------------------------------------------------------------------------------------------------------
def edit_candidate(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate Edited Successfully..')
            return redirect('admin-dashboard')
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'e_vote_blockchain/edit_candidate.html', {'form': form, 'candidate': candidate})


#---------------------------------------------------------------------------------------------------------
# DELETE CANDIDATE VIEW
#---------------------------------------------------------------------------------------------------------
def delete_candidate(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if request.method == 'POST':
        candidate.delete()
        messages.success(request, 'Candidate Deleted Successfully..')
        return redirect('b_voteapp:home')
    return render(request, 'e_vote_blockchain/delete_candidate.html', {'candidate': candidate})
