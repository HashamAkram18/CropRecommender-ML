from django.shortcuts import render, redirect
from .models import UserProfile, Prediction
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404

from .forms import UserSignupForm
from .migrations.ML.model_loader import predict_crop

# Create your views here.


def home(request):
    return render(request, "home.html") 


@login_required
def history_view(request):
    predictions = Prediction.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "history.html", {"predictions": predictions})

@login_required
def delete_prediction(request, prediction_id):
    prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user  )
    prediction.delete()
    messages.success(request, "Prediction deleted successfully")
    return redirect("history")
    
def signup_view(request):
    # Allow accessing signup even if already authenticated, for debugging or changing accounts.
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully")
            return redirect("home")
    else:
        form = UserSignupForm()

    return render(request, "signup.html", {"form": form})

def login_view(request):
    # Allow accessing login even if already authenticated, for debugging or switching users.
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        username = None
        if email:
            try:
                # Look up the user by email, then authenticate with their username
                user_obj = User.objects.get(email=email)
                username = user_obj.username
            except User.DoesNotExist:
                username = None

        user = authenticate(request, username=username, password=password) if username else None
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
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