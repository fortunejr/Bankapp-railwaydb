from django.db import models
from django.contrib.auth.models import User
from .forms import SignUpForm, AccountInformationForm
from random import randint

'''class Login_form(models.Model):
    
    firstname = models.CharField(max_length=255,blank=False, null=False)
    lastname = models.CharField(max_length=255,blank=False, null=False)
    account_number = randint(0000000000, 9999999999)
    
    def __str__(self):
        return self.name
    
    def create(self):
        self.save()'''

class Account(models.Model):
    account_name = models.CharField(max_length=60, null=False, blank=False)
    account_number = models.CharField(max_length=20, null=False,blank=False)
    account_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_account")
    account_phone = models.CharField(max_length=14, null=False, blank=False, default='0000000000')
    account_balance = models.IntegerField(default=10000.00, null=False,blank=False)
    transaction_pin = models.CharField(max_length=6, null=False, blank=False)
    date_opened = models.DateField(auto_now_add=True)
    time_opened = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.account_name

'''class TransactionHistory(models.Model):
    dr_or_cr = models.CharField(max_length=255,null=False, blank=False)
    account_history_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_owner")
    account_name = models.CharField(max_length=60, null=False, blank=False)
    account_number = models.CharField(max_length=20, null=False,blank=False)
    account_balance = models.IntegerField(default=10000.00, null=False,blank=False)
    time_of_transaction = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.dr_or_cr +" "+ self.account_name
    '''

class DebitHistory(models.Model):
    amount_debited = models.IntegerField(default=1000, null=False, blank=False)
    type = models.CharField(max_length=255, null=False, blank=False)
    account_history_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="debit_account_owner")
    account_name = models.CharField(max_length=60, null=False, blank=False)
    account_number = models.CharField(max_length=20, null=False,blank=False)
    account_balance = models.IntegerField(default=10000.00, null=False,blank=False)
    time_of_transaction = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.type +" "+ self.account_name

class CreditHistory(models.Model):
    amount_credited = models.IntegerField(default=1000, null=False, blank=False)
    type = models.CharField(max_length=255, null=False, blank=False)
    account_history_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credit_account_owner")
    account_name = models.CharField(max_length=60, null=False, blank=False)
    account_number = models.CharField(max_length=20, null=False,blank=False)
    account_balance = models.IntegerField(default=10000.00, null=False,blank=False)
    time_of_transaction = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        amount = str(self.amount_credited)
        return self.type +" "+ self.account_name + " " + amount