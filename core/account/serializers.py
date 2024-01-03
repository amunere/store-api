from django.contrib.auth.models import Group
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User
  

class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """
    email = serializers.EmailField(            
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'middle_name', 'phone']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'middle_name': {'required': True},
            'phone': {'required': True}
        }

    def create(self, validated_data):
        """
        Create and return a new User instance, given the validated data.
        """ 
        user = User.objects.create_user(**validated_data)
        return user



class RegisterSerializer(serializers.ModelSerializer):
    """
    User registeration serializer
    """
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'middle_name', 'phone')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        """
        Create and return a new User instance, given the validated data.
        """ 
        user = User.objects.create_user(**validated_data)
        return user