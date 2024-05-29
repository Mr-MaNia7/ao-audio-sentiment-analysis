from rest_framework import serializers
from .models import Contributor, CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name', 'password', 'bio', 'photo_url')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True},
            'phone_number': {'required': False},
            'updated_at': {'read_only': True},
        }

    def validate_password(self, value):
        try:
            validate_password(value, self.instance)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                validate_password(value, instance)  # Password is validated here
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__' 
