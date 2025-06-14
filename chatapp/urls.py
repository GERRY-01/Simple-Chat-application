from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('home', views.home, name='home')
]
