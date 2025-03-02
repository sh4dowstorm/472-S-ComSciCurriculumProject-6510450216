from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from ..utils.mock_data import *

class CreditVerifyView(APIView) :
    def get(self, request) :
        data = request.GET.get('uid')
        if data :
            pass            
            # get studied course of this student (enrollment)
            
            # track back to the course curriculum
            
            
            
        return Response({"status": HTTP_200_OK})
            
            