from django import forms
from django.forms import ModelForm
from . models import Voter_User, Profile
from django.contrib.auth.password_validation import validate_password

#---------------------------------------------------------------------------------------------------------
# STAFF APPOINTMENT FORM
#---------------------------------------------------------------------------------------------------------
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Voter_User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError('Passoword do not match')      
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full p-3 rounded-lg text-black'


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        
        widgets = {
            'image': forms.FileInput(),
            'bio': forms.Textarea(attrs={'rows':3})
        }