from django import forms
from b_voteapp.models import Election, Candidate

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['election_name', 'election_type','college', 'image', 'start_time', 'end_time', 'election_description', 'is_active']
        widgets = {
            'election_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded-lg',
                'placeholder': 'Election name'
            }),
            'election_type': forms.Select(attrs={
                'class': 'w-full p-2 border rounded-lg',
                'placeholder': 'Election type'
            }),
            'college': forms.Select(attrs={
                'class': 'w-full p-2 border rounded-lg'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border rounded-lg'
            }),
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full p-2 border rounded-lg'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full p-2 border rounded-lg'
            }),
            'election_description': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded-lg',
                'rows': 4,
                'placeholder': 'Describe the election...'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5'
            }),
        }



class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['election', 'image', 'name',  'role', 'party', 'description']
        widgets = {
            'election': forms.Select(attrs={
                'class': 'w-full p-2 border rounded-lg'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border rounded-lg'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded-lg',
                'placeholder': 'Candidate name'
            }),
            'role': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded-lg'
            }),
            'party': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded-lg',
                'placeholder': 'Party name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded-lg',
                'rows': 4,
                'placeholder': 'Brief description...'
            }),
        }



