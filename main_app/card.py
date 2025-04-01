from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main_app.models import CreditCard
from account.models import Account
from decimal import Decimal



def card_detail(request, card_id):
    account = Account.objects.get(user=request.user)
    card = CreditCard.objects.get(card_id=card_id, user=request.user)

    context = {
        "account":account,
        "card":card,
    }
    return render(request, "card/card-detail.html", context)


def fund_card(request, card_id):
    card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = request.user.account
    
    if request.method == "POST":
        amount = request.POST.get("funding_amount")
        
        if Decimal(amount) <= account.account_balance:
            account.account_balance -= Decimal(amount)
            account.save()
            
            card.amount += Decimal(amount)
            card.save()
            
            messages.success(request, ("Funds added to the card."))
            return redirect("main_app:card-detail", card.card_id)
        else:
            messages.warning(request, ("Insufficient Funds."))
            return redirect("main_app:card-detail", card.card_id)


def withdraw_fund(request, card_id):
    account = Account.objects.get(user=request.user)
    card = CreditCard.objects.get(card_id=card_id, user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")

        if card.amount >= Decimal(amount) and card.amount != 0.00:
            account.account_balance += Decimal(amount)
            account.save()

            card.amount -= Decimal(amount)
            card.save()

            messages.success(request, ("Successful funds withdrawal."))
            return redirect("main_app:card-detail", card.card_id)
        elif card.amount == 0.00:
            messages.warning(request, ("Insufficient Funds."))
            return redirect("main_app:card-detail", card.card_id)
        else:
            messages.warning(request, ("Insufficient Funds."))
            return redirect("main_app:card-detail", card.card_id)
        

def delete_card(request, card_id):
    card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = request.user.account
    
    if card.amount > 0:
        account.account_balance += card.amount
        account.save()

        card.delete()
        messages.success(request, ("Card deleted successfully."))
        return redirect("account:dashboard")

    card.delete()
    messages.success(request, ("Card deleted successfully."))
    return redirect("account:dashboard")