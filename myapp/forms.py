from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms 

class SignupForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'confirm_password', 'address', 'mobile_number', 'gender']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("The passwords do not match.")
   
        
    def save(self, commit=True):
        # Save the User model first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']  # Password is hashed automatically
        )
        
        # Create a UserProfile instance and associate it with the User
        profile = super(SignupForm, self).save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile

class LoginForm(forms.Form):
    username = forms.CharField( )
    password = forms.CharField(widget=forms.PasswordInput)



