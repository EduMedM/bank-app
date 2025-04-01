from django.urls import path
from account import views

app_name = "account"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("", views.account, name="account"),
    path("kyc-registration/", views.kyc_registration, name="kyc-registration"),
]
