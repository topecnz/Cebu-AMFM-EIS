from django.urls import path 
from . import views

urlpatterns = [
    path('login/', views.user_login, name="Login"),
    path('logout/', views.user_logout, name="Logout"),
    path('', views.home, name="Home")
]
