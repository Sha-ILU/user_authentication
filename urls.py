from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify/', views.verify, name='verify'),
    path('login/', views.login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
