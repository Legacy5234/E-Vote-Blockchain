from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from . models import Voter_User, Profile, College, Department
from django.contrib.auth.password_validation import validate_password

#---------------------------------------------------------------------------------------------------------
# VOTER REGISTRATION FORM
#---------------------------------------------------------------------------------------------------------
class VoterSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Voter_User
        fields = [
            'first_name', 'last_name', 'username', 'email', 
            'password', 'date_of_birth', 'gender', 'location',
            'college', 'department'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError('Passwords do not match')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full p-3 rounded-lg text-black'


#---------------------------------------------------------------------------------------------------------
# PROFILE EDIT FORM
#---------------------------------------------------------------------------------------------------------
class ProfileForm(forms.ModelForm):
    # Related Voter_User fields here
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=Voter_User.GENDER_CHOICES, required=False)
    college = forms.ModelChoiceField(queryset=College.objects.all(), required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    location = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ['image', 'bio', 'email']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['date_of_birth'].initial = user.date_of_birth
            self.fields['gender'].initial = user.gender
            self.fields['college'].initial = user.college
            self.fields['department'].initial = user.department
            self.fields['location'].initial = user.location

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none'})

    def save(self, commit=True, user=None):
        profile = super(ProfileForm, self).save(commit=False)
        if user:
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.date_of_birth = self.cleaned_data['date_of_birth']
            user.gender = self.cleaned_data['gender']
            user.college = self.cleaned_data['college']
            user.department = self.cleaned_data['department']
            user.location = self.cleaned_data['location']
            user.save()
        if commit:
            profile.save()
        return profile
