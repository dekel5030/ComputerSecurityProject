from django import forms
from accounts.models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'id_number','phone_number','city','email','package']
