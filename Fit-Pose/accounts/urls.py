#THIS WILL INCLLUDE HOME, LOGIN , REGISTER 


from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name="logout"),
    path('dashboard/profile', views.profile, name="profile"),
    path('dashboard/session/', views.session, name="session"),
    path('<int:session_id>', views.sesres, name="sessionresult"),
    path('dashboard', views.dash , name="dash"),
]
