from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import LoginWithEmailSerializer, RegistrationSerializer

class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """User registration View

        Args:
            request (request): user request

        Returns:
            data, status: return the user data with the status 200, if the infornmations was correct and 
            400 if noting was probided or if informatons provided as incorrect.
        """
        
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'fullname': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id,
            }
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = LoginWithEmailSerializer
    def post(self, request):
        """Login User View

        Args:
            request (request): request

        Returns:
            data, status: return the user data with the status 200, if the infornmations was correct 
            and 400 if noting was probided or if informatons provided as incorrect.
        """
        
        serializer = self.serializer_class(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user = user)
            data = {
                'token': token.key,
                'fullname': user.username,
                'email': user.email,
                'user_id':user.id
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'detail':'please check your username and password'}, status=status.HTTP_400_BAD_REQUEST)
       
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Logout user by delete the token in the Token database
        """
        request.user.auth_token.delete() 
        return Response({"detail": "Logout Successfully. Your Token was deleted"}, status=status.HTTP_200_OK)