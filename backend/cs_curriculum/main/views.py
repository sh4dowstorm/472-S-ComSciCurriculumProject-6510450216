from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def index(request) :
    obj = {
        'api': 'hello',
        'items': ['mango', 'banana']
    }
    return Response(obj)
