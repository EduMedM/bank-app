from django.urls import path
from main_app import views, transfer, transaction, payment_request, card

app_name = "main_app"

urlpatterns = [
    path("", views.index, name="index"),
    
    #Transfers
    path("find-account/", transfer.find_user_by_account, name="find-account"),
    path("amount-transfer/<account_number>/", transfer.amount_transfer, name="amount-transfer"),
    path("amount-transfer-process/<account_number>/", transfer.amount_transfer_process, name="amount-transfer-process"),
    path("transfer-confirmation/<account_number>/<transaction_id>/", transfer.transfer_confirmation, name="transfer-confirmation"),
    path("transfer-process/<account_number>/<transaction_id>/", transfer.transfer_process, name="transfer-process"),
    path("transfer-completed/<account_number>/<transaction_id>/", transfer.transfer_completed, name="transfer-completed"),
    
     # transactions
    path("transactions/", transaction.transaction_lists, name="transactions"),
    path("transaction-details/<transaction_id>/", transaction.transaction_details, name="transaction-details"),
    
    # Payment Request
    path("request-search-account/", payment_request.search_user_request, name="request-search-account"),
    path("amount-request/<account_number>/", payment_request.amount_request, name="amount-request"),
    path("amount-request-process/<account_number>/", payment_request.amount_request_process, name="amount-request-process"),
    path("amount-request-confirmation/<account_number>/<transaction_id>/", payment_request.amount_request_confirmation, name="amount-request-confirmation"),
    path("request-processing-permission/<account_number>/<transaction_id>/", payment_request.request_processing_permission, name="request-processing-permission"),
    path("request-completed/<account_number>/<transaction_id>/", payment_request.request_completed, name="request-completed"),
    
    # Request Settlement
    path("settlement-confirmation/<account_number>/<transaction_id>/", payment_request.settlement_confirmation, name="settlement-confirmation"),
    path("settlement-processing/<account_number>/<transaction_id>/", payment_request.settlement_processing, name="settlement-processing"),
    path("settlement-completed/<account_number>/<transaction_id>/", payment_request.settlement_completed, name="settlement-completed"),
    path("delete-request/<account_number>/<transaction_id>/", payment_request.delete_payment_request, name="delete-request"),
    
    # Card
    path("card/<card_id>/", card.card_detail, name="card-detail"),
    path("fund-card/<card_id>/", card.fund_card, name="fund-card"),
    path("withdraw_fund/<card_id>/", card.withdraw_fund, name="withdraw_fund"),
    path("delete_card/<card_id>/", card.delete_card, name="delete_card"),
]


