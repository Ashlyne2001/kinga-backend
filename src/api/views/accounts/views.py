from django.conf import settings

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authtoken.models import Token

from accounts.models import UserSession
from accounts.utils.user_type import DRIVER_USER, ADMIN_USER
from api.serializers.accounts.serializers import UserSerializer




THROTTLE_RATES = settings.THROTTLE_RATES

class TokenView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token = Token.objects.get(user=user)
        
        response_data = {
            'email': user.email,
            'name': user.get_full_name(),
            'token': token.key,
            'user_type': user.user_type,
            'reg_no': user.reg_no
        } 

        return Response(response_data)
       
class LogoutView(APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        user_sessions = UserSession.objects.filter(user = request.user)

        for user_session in user_sessions:
            user_session.session.delete()

        return Response(status=status.HTTP_200_OK)


class SignupView(APIView):
    permission_classes = ()
    """
    Creates the user.
    """
    def post(self, request, *args, **kwargs):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():

            user = serializer.save()

            token = Token.objects.get(user=user)
        
            response_data = {
                'email': user.email,
                'name': user.get_full_name(),
                'token': token.key,
                'user_type': user.user_type,
                'reg_no': user.reg_no
            } 

            return Response(response_data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)