from main.views import index
from django.urls import path

urlpatterns = [
    path('admin/', index),
]