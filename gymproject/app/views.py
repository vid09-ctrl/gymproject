from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from .models import User 
from django.contrib import messages
import re
from django.core.mail import send_mail


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

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"New Contact Message from {name}"
        message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        send_mail(
            subject,
            message_body,
            email, 
            ['nanawarevidya33@gmail.com'], 
            fail_silently=False,
        )
        messages.success(request, "Message sent successfully!")
        return redirect('contact')  

    return render(request, "contact.html")

def facilities(req):
    return render(req, "facilities.html")

def free_trial_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        # Send email to admin
        subject = "New Free Trial Request"
        message = f"New trial request:\n\nName: {name}\nEmail: {email}\nPhone: {phone}"
        from_email = "nanawarevidya33@gmail.com"  # must match EMAIL_HOST_USER
        to_email = ["nanaware406@gmail.com"]  # can be list of admin emails

        send_mail(subject, message, from_email, to_email)

        # Optional: send confirmation to user
        send_mail(
            subject="Thank You for Requesting a Free Trial at PowerFlex Gym!",
            message=f"Hi {name},\n\nThanks for your interest! We'll contact you shortly.\n\n- PowerFlex Gym",
            from_email=from_email,
            recipient_list=[email]
        )

        messages.success(request, "Your request has been submitted! We'll contact you soon.")
        return redirect('free_trial')

    return render(request, 'free_trial.html')


def forgot(req):
    if req.method == "GET":
        return render(req, "forgot.html")

    uname = req.POST.get("uname").strip()

    # Validation Checks
    if not uname:
        messages.error(req, "Username field cannot be empty!")
        return redirect("forgot")  # ✅ Corrected

    if len(uname) < 3:
        messages.error(req, "Username must be at least 3 characters long!")
        return redirect("forgot")  # ✅ Corrected

    if not User.objects.filter(username=uname).exists():
        messages.error(req, "User not found. Please enter a valid username!")
        return redirect("forgot")  # ✅ Corrected

    return redirect("resetpassword", uname=uname)


def resetpassword(req, uname):
    if req.method == "GET":
        print("Reset password GET request received")  # <-- Check terminal
        return render(req, "resetpassword.html", {"uname": uname})
    upass = req.POST.get("new_password", "").strip()
    confirm_pass = req.POST.get("confirm_password", "").strip()

    if not upass or not confirm_pass:
        messages.error(req, "Password fields cannot be empty!")
        return redirect("resetpassword", uname=uname)

    if upass != confirm_pass:
        messages.error(req, "Passwords do not match!")
        return redirect("resetpassword", uname=uname)

    # Custom Strength Checks
    if len(upass) < 8:
        messages.error(req, "Password must be at least 8 characters long!")
        return redirect("resetpassword", uname=uname)

    if not re.search(r"[A-Z]", upass):
        messages.error(req, "Password must contain at least one uppercase letter (A-Z)!")
        return redirect("resetpassword", uname=uname)

    if not re.search(r"[a-z]", upass):
        messages.error(req, "Password must contain at least one lowercase letter (a-z)!")
        return redirect("resetpassword", uname=uname)

    if not re.search(r"\d", upass):
        messages.error(req, "Password must contain at least one number (0-9)!")
        return redirect("resetpassword", uname=uname)

    if not re.search(r"[!@#$%^&*(),.?]", upass):
        messages.error(req, "Password must contain at least one special character (!@#$%^&*)!")
        return redirect("resetpassword", uname=uname)

    # Try saving password
    try:
        validate_password(upass)
        userdata = User.objects.get(username=uname)
        userdata.set_password(upass)
        userdata.save()
        messages.success(req, "Password reset successful! You can now sign in.")
        return redirect("signin")
    except User.DoesNotExist:
        messages.error(req, "User not found!")
        return redirect("forgot")
    except ValidationError as e:
        messages.error(req, ", ".join(e.messages))
        return redirect("resetpassword", uname=uname)

def success(request):
    return render(request, 'success.html')