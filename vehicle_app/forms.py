from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
    
    def clean_vehicle_number(self):
        vehicle_number = self.cleaned_data['vehicle_number']
        if not vehicle_number.isalnum():
            raise forms.ValidationError("Vehicle number must contain only alphanumeric characters.")
        return vehicle_number