from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder':'Your Email address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Repeat password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    


class AccountInformationForm(forms.Form):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'transaction_pin']
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Your Firstname',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Your Lastname',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder':'Your Phone number',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    transaction_pin = forms.IntegerField(widget=forms.TextInput(attrs={
        'placeholder':'Your Transaction Pin',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))


class MakeTransfer(forms.Form):
    class Meta:
        model = User
        fields = ['account_number', 'amount']
    account_number = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"The receiver's account number",
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    amount = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"The amount to transfer",
        'class': 'w-full py-4 px-6 rounded-xl'
    }))


class ConfirmTransactionPin(forms.Form):
    transaction_pin = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Your transaction pin",
            'class': 'w-full py-4 px-6 rounded-xl'
        })
    )