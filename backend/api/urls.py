from django.urls import path

from main.views import CreditVerifyView

urlpatterns = [
    path('credit-verify/', CreditVerifyView.as_view(), name='credit-verify-view')
]