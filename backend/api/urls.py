from main.views import *
from django.urls import path

urlpatterns = [
    path('admin/', index),
    path('signup/', signup_with_otp, name='signup_with_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('complete-registration/', complete_registration, name='complete_registration'),
]