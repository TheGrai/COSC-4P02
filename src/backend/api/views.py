from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def generateMessageResponse(request):
    response = 'Received Message: ' + request.query_params['message']
    return Response({'message': response})
