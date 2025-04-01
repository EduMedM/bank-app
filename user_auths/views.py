from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from user_auths.forms import UserRegisterForm
from user_auths.models import User

def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, ("You are already logged in."))
        return redirect("account:account")
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, ("Your account was successfully created."))
            new_user = authenticate(username=form.cleaned_data['email'], 
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("account:account")
        
    else:
        form = UserRegisterForm()
    context = {
        "form": form
    }
    return render(request, "user_auths/sign-up.html", context)

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")    
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, ("You are logged."))
                return redirect("account:account")
            else:
                messages.warning(request, ("Username or password does not match."))
                return redirect("user_auths:sign-in")
        except:
            messages.warning(request, ("User does not exist."))
    
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged In")
        return redirect("account:account")
    
    return render(request, "user_auths/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request, ("You have been logged out."))
    return redirect("user_auths:sign-in")
