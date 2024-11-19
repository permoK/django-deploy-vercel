# urls.py
from django.urls import path
from .views import FarmerRegistrationView, LoginView, LogoutView, CowView, FarmerDetailView, ping_serverless, index

urlpatterns = [
    path('register/', FarmerRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('farmerData/', FarmerDetailView.as_view(), name='farmerData'),
    path('farmers/', FarmerDetailView.as_view(), name='farmers'),
    path('cows/', CowView.as_view(), name='cows'),
    path('cows/<int:cow_id>/', CowView.as_view(), name='cows'),

    # Warming up the server 
    path('ping-serverless/', ping_serverless, name='ping_serverless'),
]

