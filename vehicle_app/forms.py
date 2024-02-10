from django import forms
from .models import Vehicle
from .models import UserGroup
from django.contrib.auth.forms import UserCreationForm
from .models import UserGroup
from django.contrib.auth.models import User

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
    
    def clean_vehicle_number(self):
        vehicle_number = self.cleaned_data['vehicle_number']
        if not vehicle_number.isalnum():
            raise forms.ValidationError("Vehicle number must contain only alphanumeric characters.")
        return vehicle_number


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','password']




class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())