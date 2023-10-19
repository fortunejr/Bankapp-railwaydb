from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ConfirmTransactionPin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from random import randint
from .models import *
from .forms import MakeTransfer


def gen_account_number():
    generated_account_number = randint(0000000000, 9999999999)
    return generated_account_number

# Create your views here.
# Home page
def index(request):
    return render(request, 'core/index.html')

# Account Info Form
def account_info(request):
    if request.method == 'POST':
        form = AccountInformationForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = form.cleaned_data['first_name']
            request.session['last_name'] = form.cleaned_data['last_name']
            request.session['phone'] = form.cleaned_data['phone']
            request.session['transaction_pin'] = form.cleaned_data['transaction_pin']
            
            return redirect('/signup/')
            
    else:
        messages.info(request, "Please provide accurate informations")
        form = AccountInformationForm()
    return render(request, 'core/account_info.html', {
        'form':form,
    })

# Signup function
def signup(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            user = User.objects.create_user(
                username = username,
                email = email,
                password = password
            )
            user.save()
            
            
            
            firstname = request.session['first_name']
            lastname = request.session['last_name']
            phone = request.session['phone']
            transaction_pin1 = request.session['transaction_pin']
            
            account = Account.objects.create(
                account_name = firstname + " " + lastname,
                account_number = gen_account_number(),
                account_owner = user,
                account_phone = phone,
                transaction_pin = transaction_pin1,
            )
            account.save()
            messages.success(request, "Account created ")
            login(request, user)
            return redirect('/profile/')
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {
        'form': form,
        
    })





def login_user(request):
    if request.user.is_authenticated:
        return redirect('core:account')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            # Authenticating process
            if user is not None:
                login(request, user)
                return redirect('accounts')
            else:
                messages.info(request, ' Username or Password is incorrect')
        
        return render(request, 'core/login.html')

# Account view
@login_required(login_url='core:login')
def dashboard(request):
    profile =  Account.objects.filter(account_owner=request.user)
    return render(request, 'accounts/profile.html', {
        'profile':profile,
    })
    
    
@login_required
def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")

# transfer of money
@login_required(login_url='core:login')
def transfer(request):
    
    if request.method == 'POST':
        form = MakeTransfer(request.POST)
        print('request not having issues')
        if form.is_valid():
            print('form is valid')
            global reciever_account
            reciever_account = form.cleaned_data['account_number']
            global amount
            amount = form.cleaned_data['amount']
            request.session['reciever_account'] = reciever_account
            request.session['amount'] = amount
            
            chk_account =  Account.objects.filter(account_number=reciever_account)
            for a in chk_account:
                account_name = a.account_name
            
            if chk_account.count():
                global reciever_name
                reciever_name = account_name
                request.session['reciever_name'] = reciever_name
                print('bla bla')
                
            user_account = Account.objects.filter(account_owner=request.user)
                
            for u in user_account:
                account_balance = int(u.account_balance)
            
            
            
            
            if not chk_account.count():
                messages.error(request, "Unable to find user with this account")
                print('no user')
                return render(request, "transfer/make-transfer.html", {"form":form})
            
            # if amount is greater than user account balance 
            if int(amount) > account_balance:
                messages.error(request, "You do not have enough money in your account")
                print('insufficient funds')
                return render(request, "transfer/make-transfer.html", {"form":form})
            
            
            # redirects to confirm the transaction
            if account_balance > int(amount):
                print('good to go')
                return redirect('/confirmation/')
            else:
                messages.error(request, "Insufficient funds")
                print('not good to go')
                return render(request, "transfer/make-transfer.html", {"form":form})
                
        else:
            messages.error(request, "Please provide the required details to continue with your transaction")
            print('form not valid')
            return render(request, "core/login.html", {"form":form})
        
        
    else:
        form = MakeTransfer()
    account = Account.objects.filter(account_owner=request.user)
    print('error here')
    return render(request, 'transfer/make-transfer.html',{
        'form':form,
        'account':account,
    })

@login_required(login_url='core:login')
def confirm_transaction(request):
    if request.method=='POST':
        form = ConfirmTransactionPin(request.POST)
        if form.is_valid():
            print('form is valid')
            transaction_pin = form.cleaned_data['transaction_pin']
            request.session['transaction_pin'] = transaction_pin
            print(transaction_pin)
            
            sender = Account.objects.get(account_owner=request.user)
            if transaction_pin == sender.transaction_pin:
                # sender account name 
                sender_name = sender.account_name
                # sender_account = Account.objects.get(account_number=request.user)
                # sender bal before transaction 
                sender_bal_before_transaction = sender.account_balance
                #deduct amount from sender bal 
                new_sender_balance = int(sender.account_balance) - int(amount)
                #sender new balance
                sender.account_balance = new_sender_balance
                sender.save()
                # sender bal after transaction 
                sender_bal_after_transaction = sender.account_balance 
                
                
                #fetch receiver account
                reciever = Account.objects.get(account_number=reciever_account)
                reciever_user = Account.objects.get(account_number=reciever_account)
                #reciever name 
                reciever_account_name = reciever.account_name
                # reciever bal before transaction 
                reciever_bal_before_transaction = reciever.account_balance
                # add amount to receiver bal 
                new_reciever_balance = int(reciever.account_balance) + int(amount)
                # reciever new balance
                reciever.account_balance = new_reciever_balance
                reciever.save()
                # reciever bal after transaction 
                reciever_bal_after_transaction = reciever.account_balance
                
                sender_history = DebitHistory.objects.create(
                    amount_debited = amount,
                    type = 'DEBIT',
                    account_history_owner = request.user,
                    account_name = reciever_account_name,
                    account_number = sender.account_number,
                    account_balance = sender_bal_after_transaction
                )
                sender_history.save()
                
                reciever_history = CreditHistory.objects.create(
                    amount_credited = amount,
                    type = 'CREDIT',
                    account_history_owner = reciever.account_owner,
                    account_name = sender_name,
                    account_number = reciever_account,
                    account_balance = reciever_bal_after_transaction
                )
                reciever_history.save()
                
                messages.success(request, "Transfer successful")
                return redirect("/profile/")
            else:
                messages.error(request, "Invalid transaction pin")
                return render(request, "transfer/confirm-transfer.html")
        else:
            messages.error(request, "Unable to perform transaction, please try again later")
            return render(request, "transfer/confirm-transfer.html")
    form = ConfirmTransactionPin(request.POST) 
    return render(request, 'transfer/confirm-transfer.html', {
        'reciever_account':reciever_account,
        'amount':amount,
        'reciever_name':reciever_name,
    })


def transactions(request):
    credit_history = CreditHistory.objects.filter(account_history_owner=request.user)
    debit_history = DebitHistory.objects.filter(account_history_owner=request.user)
    return render(request, 'accounts/transactions.html',{
        'credit_history':credit_history,
        'debit_history':debit_history,
    })