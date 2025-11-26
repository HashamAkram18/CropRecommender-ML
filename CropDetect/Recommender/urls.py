from django.urls import path
from .views import *  


urlpatterns = [
    path("", home, name="home"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # path("dashboard/", dashboard_view, name="dashboard"),
    path("predict/", predict_view, name="predict"),
#     path("history/", history_view, name="history"),
#     path("export/", export_view, name="export"),
#     path('predict/', create_prediction, name='prediction_create'),
#     path('history/', history, name='prediction_history'),
#     path('predictions/', predictions_list, name='predictions_list'),
#     path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
]