from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from .models import User 
from django.contrib import messages

# Home Page
def index(request):
    return render(request, 'index.html')


# Sign In View
def signin(req):
    if req.method == "GET":
        return render(req, "signin.html")

    uname = req.POST.get("uname", "").strip()
    upass = req.POST.get("upass", "").strip()
    context = {}

    if not uname or not upass:
        context["errmsg"] = "Fields can't be empty"
        return render(req, "signin.html", context)

    userdata = authenticate(username=uname, password=upass)

    if userdata is not None:
        login(req, userdata)
        return redirect("index")
    else:
        context["errmsg"] = "Invalid username or password"
        return render(req, "signin.html", context)


# Logout View
def logout_view(request):
    logout(request)
    return redirect('signin')  # Assuming 'signin' is the correct name


# Sign Up View
def signup(req):
    if req.method == "GET":
        return render(req, "signup.html")

    uname = req.POST.get("uname", "").strip()
    upass = req.POST.get("upass", "").strip()
    ucpass = req.POST.get("ucpass", "").strip()
    context = {}

    if not uname or not upass or not ucpass:
        context["errmsg"] = "Fields can't be empty"
    elif upass != ucpass:
        context["errmsg"] = "Password and Confirm Password do not match"
    elif upass == uname:
        context["errmsg"] = "Password cannot be the same as username"
    else:
        try:
            validate_password(upass)
            user = User.objects.create_user(username=uname, password=upass)
            return redirect("signin")
        except IntegrityError:
            context["errmsg"] = "Username already exists"
        except ValidationError as e:
            context["errmsg"] = ", ".join(e.messages)
        except Exception:
            context["errmsg"] = "An unexpected error occurred"

    return render(req, "signup.html", context)

def about(req):
    return render(req, "about.html")

def contact(req):
    return render(req, "contact.html")

def facilities(req):
    return render(req, "facilities.html")


def free_trial(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # Save or process data
        messages.success(request, "Thanks! We'll contact you soon.")
        return redirect('index')
    return render(request, 'free_trial.html')
