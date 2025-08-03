from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *

class RegistrationSerializer(serializers.ModelSerializer):
    
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = UserModel
        fields = "__all__"
        
    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
        )
        user.save()
        return user
    


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = f"{user.id}"
        token['name'] =user.name
        token['email'] = user.email
        token['superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        token['is_acitve'] = user.is_active
        return token
    
    def validate(self, attrs):
        user = self.context['user']

        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }