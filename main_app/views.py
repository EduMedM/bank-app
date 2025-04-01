from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # if request.user.is_authenticated:
    #     return redirect("account:account")
    return render(request, "main_app/index.html")

def contact(request):
    return render(request, "main_app/contact.html")

def about(request):
    return render(request, "main_app/about.html")

