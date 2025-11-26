from django.shortcuts import render, redirect
from .models import UserProfile, Prediction
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import UserSignupForm
from .migrations.ML.model_loader import predict_crop

# Create your views here.

def home(request):
    return render(request, "home.html") 

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully")
            return redirect("home")
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home") 

def predict_view(request):
    if request.method == "POST":
        feature_dict = {
            "nitrogen": request.POST.get("nitrogen"),
            "phosphorus": request.POST.get("phosphorus"),
            "potassium": request.POST.get("potassium"),
            "temperature": request.POST.get("temperature"),
            "humidity": request.POST.get("humidity"),
            "ph": request.POST.get("ph"),
            "rainfall": request.POST.get("rainfall"),
        }
        
        # Ensure correct order for the model: N, P, K, Temp, Humidity, pH, Rainfall
        features_list = [
            feature_dict["nitrogen"],
            feature_dict["phosphorus"],
            feature_dict["potassium"],
            feature_dict["temperature"],
            feature_dict["humidity"],
            feature_dict["ph"],
            feature_dict["rainfall"]
        ]
        
        predicted_label = predict_crop(features_list)
        
        # Save prediction to database only if user is authenticated
        if request.user.is_authenticated:
            Prediction.objects.create(
                user=request.user, 
                predicted_label=predicted_label, 
                **feature_dict
            )
            messages.success(request, "Prediction successful")
        else:
            messages.success(request, "Prediction successful (Log in to save to history)")
        
        return render(request, "predict.html", {"prediction": predicted_label.title()})
            
    return render(request, "predict.html")