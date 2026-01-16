from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import LoginWithEmailSerializer, RegistrationSerializer, CustomTokenObtainPairSerializer

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
            data = {
                'fullname': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id,
            }
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        """Override the post method to set the JWT token in an HttpOnly cookie.
        Args:
            request (request): user request
        Returns:
            response: response with the JWT token set in an HttpOnly cookie.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']
        
        response = Response({"message":"Login successfully"}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=str(access),
            httponly=True,
            secure=False,
            samesite='Lax',
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite='Lax',
        )
        response.data = {'message': 'Login successful'}
        return response


class CookieTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        """Override the post method to refresh the JWT token from HttpOnly cookie.

        Args:
            request (request): user request
        Returns:
            response: response with the refreshed JWT token set in an HttpOnly cookie.
        """
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'refresh': refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        access = serializer.validated_data.get('access')
        response = Response({'message': 'Token refreshed successfully'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=False,
            samesite='Lax',
        )
        return response
            
            
            
            
            
            
            
            
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
            data = {
                'fullname': user.username,
                'email': user.email,
                'user_id':user.id
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'detail':'please check your username and password'}, status=status.HTTP_400_BAD_REQUEST)
       