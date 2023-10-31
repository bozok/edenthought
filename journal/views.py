from django.shortcuts import render, redirect

from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate

from .forms import NewUserForm, LoginUserForm, ThougtForm, UpdateProfileForm, UpdateProfilePictureForm

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import Thought, Profile

from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def index(request):
    return render(request, "journal/index.html")

def register(request):
    form=NewUserForm()
    if request.method=="POST":
        form=NewUserForm(request.POST)
        if form.is_valid():
            current_user=form.save(commit=False)
            form.save()
            send_mail("Welcome to Edentought!", "Congratulations on creating your account", settings.DEFAULT_FROM_EMAIL, [current_user.email])
            profile=Profile.objects.create(user=current_user)
            messages.success(request, "Registration complete!")
            return redirect("login")
    context={"form": form}
    return render(request, "journal/register.html", context)

def login(request):
    form=LoginUserForm()
    if request.method=="POST":
        form=LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username=request.POST.get("username")
            password=request.POST.get("password")
            user=authenticate(request, username=username, password=password)
            if user:
                auth_login(request,user)
                return redirect("dashboard")
    context={"form":form}
    return render(request, "journal/login.html", context)

def logout(request):
    auth_logout(request)
    return redirect("index")

@login_required(login_url="login")
def dashboard(request):
    profile_pic=Profile.objects.get(user=request.user)
    context={"profilePic": profile_pic}
    return render(request, "journal/dashboard.html", context)

@login_required(login_url="login")
def new_thought(request):
    form=ThougtForm()
    if request.method == "POST":
        form = ThougtForm(request.POST)
        if form.is_valid():
            thought=form.save(commit=False)
            thought.user=request.user
            thought.save()
            messages.success(request, "New thought created!")
            return redirect("my-thoughts")
    context={"form": form}
    return render(request, "journal/new-thought.html", context)

@login_required
def my_thoughts(request):
    current_user = request.user.id
    thoughts = Thought.objects.filter(user=current_user)
    context={"thoughts":thoughts}
    return render(request, "journal/my-thoughts.html", context)

@login_required(login_url="login")
def update_thought(request, pk):
    try:
        thought = Thought.objects.get(pk=pk,user=request.user)
    except:
        return redirect("my-thoughts")
    form = ThougtForm(instance=thought)
    if request.method == "POST":
        form = ThougtForm(request.POST, instance=thought)
        if form.is_valid():
            form.save()
            messages.success(request, "Thought updated!")
            return redirect("my-thoughts")
    context={"form":form}
    return render(request, "journal/update-thought.html", context)

@login_required(login_url="login")
def delete_thought(request, pk):
    try:
        thought = Thought.objects.get(pk=pk,user=request.user)
    except:
        return redirect("my-thoughts")
    if request.method == "POST":
        thought.delete()
        messages.success(request, "Thought deleted!")
        return redirect("my-thoughts")
    return render(request, "journal/delete-thought.html")

@login_required(login_url="login")
def profile_management(request):
    form=UpdateProfileForm(instance=request.user)
    profile=Profile.objects.get(user=request.user)
    form_pic=UpdateProfilePictureForm(instance=profile)
    if request.method=="POST":
        form=UpdateProfileForm(request.POST, instance=request.user)
        form_pic=UpdateProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
        if form_pic.is_valid():
            form_pic.save()
            return redirect("dashboard")
    context={"form": form, "form_pic":form_pic}
    return render(request, "journal/profile-management.html", context)

@login_required(login_url="login")
def delete_account(request):
    if request.method=="POST":
        deleteUser=User.objects.filter(username=request.user)
        deleteUser.delete()
        return redirect("index")
    return render(request, "journal/delete-account.html")

