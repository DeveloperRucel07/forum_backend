from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginWithEmailSerializer(serializers.ModelSerializer):
    """
    Login Serializer.
    read all login informations
    validate if the information are corresponding to the pretent user or not.
    
    """
    email = serializers.CharField()
    password = serializers.CharField(write_only= True)
    
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
    
    def validate(self, data):
        """
        Validate the login data by checking email and password.

        Args:
            data (dict): The data to validate containing email and password.

        Returns:
            dict: The validated data with user added.

        Raises:
            ValidationError: If email or password is invalid.
        """
        email = data.get('email')
        password = data.get('password')  
        try:
            user = User.objects.get(email=email)
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
        