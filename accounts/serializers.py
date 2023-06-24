from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'phone', 'name', 'password', 'is_staff')

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            phone=validated_data['phone']
        )

        if validated_data['is_staff'] == True:
            user.is_staff = True

        user.set_password(validated_data['password'])
        user.save()
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        if not user or not user.check_password(attrs['password']):
            raise serializers.ValidationError('Incorrect email or password')
        
        refresh = RefreshToken.for_user(user)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        return attrs
    

class RetrieveCoachesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'phone')