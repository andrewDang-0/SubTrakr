from django import forms
from .models import Subscription
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'price', 'billing_cycle', 'renewal_date', 'remind_method', 'category']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")