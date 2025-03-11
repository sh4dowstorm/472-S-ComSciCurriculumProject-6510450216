from django.urls import path

from main.views import CreditVerifyView, FileUploadView

urlpatterns = [
    path('credit-verify/', CreditVerifyView.as_view(), name='credit-verify-view'),
    path('upload/', FileUploadView.as_view(), name='file-upload-view')
]