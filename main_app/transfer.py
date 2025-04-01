from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal

from main_app.models import Transaction#, Notification
from account.models import Account, KYC

@login_required
def find_user_by_account(request):
    user = request.user
    account = Account.objects.get(user=user)
    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None
        
    accounts = Account.objects.all()
    query = request.POST.get("account_number") 
    
    if query:
        accounts = accounts.filter(
            Q(account_number=query)|
            Q(account_id=query)
        ).distinct()
        
    print(accounts)
    print(query)
    
    context = {
        "accounts": accounts,
        "query": query,
        "kyc": kyc,
        "account": account,
    }
    return render(request, "transfer/find-user-by-account-number.html", context)


def amount_transfer(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except:
        messages.warning(request, ("Account does not exist."))
        return redirect("main_app:find-account")
    context = {
        "account": account,
    }
    return render(request, "transfer/amount-transfer.html", context)


def amount_transfer_process(request, account_number):
    account = Account.objects.get(account_number=account_number)
    sender = request.user
    receiver = account.user

    sender_account = request.user.account
    receiver_account = account

    if request.method == "POST":
        amount = request.POST.get("amount-send")
        description = request.POST.get("description")

        print(amount)
        print(description)

        if sender_account.account_balance >= Decimal(amount):
            new_transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                description=description,
                receiver=receiver,
                sender=sender,
                sender_account=sender_account,
                receiver_account=receiver_account,
                status="processing",
                transaction_type="transfer"
            )
            new_transaction.save()
            
            transaction_id = new_transaction.transaction_id
            return redirect("main_app:transfer-confirmation", account.account_number, transaction_id)
        else:
            messages.warning(request, ("Insufficient Funds."))
            return redirect("main_app:amount-transfer", account.account_number)
    else:
        messages.warning(request, ("Error Occurred. Try again later."))
        return redirect("account:account")
    
    
def transfer_confirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, ("Transaction does not exist."))
        return redirect("account:account")
    context = {
        "account":account,
        "transaction":transaction
    }
    return render(request, "transfer/transfer-confirmation.html", context)


def transfer_process(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    sender = request.user 
    sender_account = request.user.account 

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        print(pin_number)

        if pin_number == sender_account.pin_number:
            transaction.status = "completed"
            transaction.save()

            sender_account.account_balance -= transaction.amount
            sender_account.save()

            account.account_balance += transaction.amount
            account.save()
            
            # Notification.objects.create(
            #     amount=transaction.amount,
            #     user=account.user,
            #     notification_type="Credit Alert"
            # )
            
            # Notification.objects.create(
            #     user=sender,
            #     notification_type="Debit Alert",
            #     amount=transaction.amount
            # )

            messages.success(request, ("Transfer Successful."))
            return redirect("main_app:transfer-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, ("Incorrect Pin."))
            return redirect('main_app:transfer-confirmation', account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, ("An error occurred, Try again later."))
        return redirect('account:account')
    
def transfer_completed(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transfer does not exist.")
        return redirect("account:account")
    context = {
        "account":account,
        "transaction":transaction
    }
    return render(request, "transfer/transfer-completed.html", context)