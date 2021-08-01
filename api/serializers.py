from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from user_management.models import CustomUser, Organization


class SignUprSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ('first_name', 'email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('id', 'name', 'owner', 'members')

    def validate_name(self, value):
        if value:
            if Organization.objects.filter(name=value).exclude(id=self.context.get('pk')).exists():
                raise serializers.ValidationError('Name "%s" is already in use.' % value)
            else:
                return value
        else:
            raise serializers.ValidationError('This field is required.')

