from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal

from main_app.models import Transaction
from account.models import Account

@login_required
def search_user_request(request):
    accounts = Account.objects.all()
    query = request.POST.get("account_number")

    if query:
        accounts = accounts.filter(
            Q(account_number=query)|
            Q(account_id=query)
        ).distinct()
    
    context = {
        "accounts": accounts,
        "query": query,
    }
    return render(request, "payment_request/request-search-account.html", context)

def amount_request(request, account_number):
    account = Account.objects.get(account_number=account_number)
    context = {
        "account": account,
    }
    return render(request, "payment_request/amount-request.html", context)


def amount_request_process(request, account_number):
    account = Account.objects.get(account_number=account_number)

    sender = request.user
    receiver = account.user

    sender_account = request.user.account
    receiver_account = account

    if request.method == "POST":
        amount = request.POST.get("amount-request")
        description = request.POST.get("description")

        new_request = Transaction.objects.create(
            user=request.user,
            amount=amount,
            description=description,

            sender=sender,
            receiver=receiver,

            sender_account=sender_account,
            receiver_account=receiver_account,

            status="request_processing",
            transaction_type="request"
        )
        new_request.save()
        transaction_id = new_request.transaction_id
        return redirect("main_app:amount-request-confirmation", account.account_number, transaction_id)
    else:
        messages.warning(request, ("Error Occurred, try again later."))
        return redirect("account:dashboard")
    
    
def amount_request_confirmation(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "account":account,
        "transaction":transaction,
    }
    return render(request, "payment_request/amount-request-confirmation.html", context)


def request_processing_permission(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number:
            transaction.status = "request_sent"
            transaction.save()
            
            # Notification.objects.create(
            #     user=account.user,
            #     notification_type="Recieved Payment Request",
            #     amount=transaction.amount,
                
            # )
            
            # Notification.objects.create(
            #     user=request.user,
            #     amount=transaction.amount,
            #     notification_type="Sent Payment Request"
            # )

            messages.success(request, ("Your payment request have been sent successfully."))
            return redirect("main_app:request-completed", account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, ("An Error Occurred. Try again later."))
        return redirect("account:dashboard")
    
def request_completed(request, account_number ,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
            "account":account,
            "transaction":transaction,
        }
    return render(request, "payment_request/request-completed.html", context)


def settlement_confirmation(request, account_number ,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
            "account":account,
            "transaction":transaction,
        }
    return render(request, "payment_request/settlement-confirmation.html", context)


def settlement_processing(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    sender = request.user 
    sender_account = request.user.account

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number:
            if sender_account.account_balance <= 0 or sender_account.account_balance < transaction.amount:
                messages.warning(request, ("Insufficient Funds."))
            else:
                sender_account.account_balance -= transaction.amount
                sender_account.save()

                account.account_balance += transaction.amount
                account.save()

                transaction.status = "request_settled"
                transaction.save()

                messages.success(request, (f"Transfer to {account.user.kyc.full_name} was successful."))
                return redirect("main_app:settlement-completed", account.account_number, transaction.transaction_id)

        else:
            messages.warning(request, ("Incorrect Pin"))
            return redirect("main_app:settlement-confirmation", account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, ("Error Occurred"))
        return redirect("account:dashboard")
    
    
def settlement_completed(request, account_number ,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
            "account":account,
            "transaction":transaction,
        }
    return render(request, "payment_request/settlement-completed.html", context)


def delete_payment_request(request, account_number ,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    print(f"(request receiver) -> account.user: {account.user} == transaction.receiver: {transaction.receiver}")

    if request.user == transaction.user or account.user == transaction.receiver:
        transaction.delete()
        messages.success(request, ("Payment Request Deleted Successfully"))
        return redirect("main_app:transactions")
    