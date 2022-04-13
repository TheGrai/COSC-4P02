from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def generateMessageResponse(request):
    response = 'Recieved Message: ' + request.query_params['message'] + '. Have a great Day!'
    return Response({'message': response})