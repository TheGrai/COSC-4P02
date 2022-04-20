from rest_framework.decorators import api_view
from rest_framework.response import Response
from chatbot.chatbot_brock import respond as b_respond
from chatbot.chatbot_cg import respond as cg_respond


@api_view(['GET'])
def generateMessageResponse(request):
    if 'message' in request.query_params:
        response = 'Received Message: ' + request.query_params['message']
        return Response({'message': response})
    if 'brock' in request.query_params:
        return Response({'message': b_respond(request.query_params['brock'])})
    if 'cg' in request.query_params:
        return Response({'message': cg_respond(request.query_params['cg'])})
