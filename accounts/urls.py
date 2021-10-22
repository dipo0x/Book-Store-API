from .import views
from .views import LoginAPI
from django.urls import path

urlpatterns = [
    path('accounts/login/', LoginAPI.as_view(), name="login"),
    path('profile', views.profile, name="profile"),
    path('register', views.register),
    path('logout', views.logout_user)
] 
