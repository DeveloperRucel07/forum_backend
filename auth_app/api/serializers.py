from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth  import get_user_model

User = get_user_model()

class LoginWithEmailSerializer(serializers.ModelSerializer):
    """
    Login Serializer.
    read all login informations
    validate if the information are corresponding to the pretent user or not.
    
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only= True)
    
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
    
    def validate(self, data):
        """
        Validate the login data by checking username and password.

        Args:
            data (dict): The data to validate containing username and password.

        Returns:
            dict: The validated data with user added.

        Raises:
            ValidationError: If username or password is invalid.
        """
        user = data.get('username')
        password = data.get('password')  
        try:
            user = User.objects.get(username=user)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        user = authenticate(username=user.username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        data['user'] = user
        return data

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Registration Serializer.
    read all registration informations
    write the fullname by assigning it to the username
    validate if the both password are correct or not.
    
    """
    repeated_password = serializers.CharField(write_only = True)
    fullname = serializers.CharField()
    class Meta:
        model = User
        fields = ['fullname', 'email','password', 'repeated_password']
        extra_kwargs = {
            'password':{
                'write_only': True
            }
        }
        
    def save(self):
        """ if all required informations was correct, create a user.

        Raises:
            serializers.ValidationError: password don't match
            serializers.ValidationError: the email already exists

        Returns:
            user data: a user information
        """
        
        
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        
        if pw != repeated_pw:
            raise serializers.ValidationError({'error':'passwords dont match'})
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'this Email already exists'})
        
        account = User(email = self.validated_data['email'], username = self.validated_data['fullname'])
        account.set_password(pw)
        account.save()
        return account
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom Token Obtain Pair Serializer.
    Used to customize the token claims if needed.
    Currently, it does not add any additional claims.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'username' in self.fields:
            self.fields.pop('username')
        
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")
        
        data = super().validate({'username': user.username, 'password': password})
        return data
        
        
    
    
        