from django.db import transaction

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from user_management.models import CustomUser, Organization, PersonalPassword, OrganizationPassword, \
OrganizationPasswordAccessLevel


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


class PersonalPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalPassword
        fields = ('id', 'site', 'login_url', 'username', 'password', 'owner', 'users')


class OrganizationPasswordSerializer(serializers.ModelSerializer):
    users = serializers.ListField(write_only=True)

    class Meta:
        model = OrganizationPassword
        fields = ('id', 'site', 'login_url', 'username', 'password', 'organization', 'users')

    @transaction.atomic
    def create(self, validated_data):
        organization_password = OrganizationPassword.objects.create(
            site=validated_data['site'],
            login_url=validated_data['login_url'],
            username=validated_data['username'],
            password=validated_data['password'],
            organization=validated_data['organization']
        )
        if validated_data.get('users'):
            for each in validated_data.get('users'):
                OrganizationPasswordAccessLevel.objects.create(
                    organization_password=organization_password,
                    user_id=each.get('user'),
                    access_level=each.get('access_level')
                )
        return organization_password

    @transaction.atomic
    def update(self, instance, validated_data):
        if validated_data.get('site'):
            instance.site = validated_data.get('site')
        if validated_data.get('login_url'):
            instance.login_url = validated_data.get('login_url')
        if validated_data.get('username'):
            instance.username = validated_data.get('username')
        if validated_data.get('password'):
            instance.password = validated_data.get('password')
        if validated_data.get('organization'):
            instance.organization = validated_data.get('organization')

        instance.users.clear()
        instance.save()

        users = validated_data.pop('users')
        if users:
            for each in users:
                OrganizationPasswordAccessLevel.objects.create(
                    organization_password=instance,
                    user_id=each.get('user'),
                    access_level=each.get('access_level')
                )
        return instance
