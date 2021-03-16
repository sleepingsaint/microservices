from rest_framework import serializers, exceptions
from .models import CustomUser as User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

from allauth.utils import email_address_exists, get_username_max_length
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = self._validate_email(email, password)

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=10)
    last_name = serializers.CharField(max_length=10)
    password = serializers.CharField(write_only=True)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        user = User.objects.filter(username=username)

        if len(user) > 0:
            raise serializers.ValidationError(
                _("A user is already registered with this username."))

        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if email and email_address_exists(email):
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."))
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar',
                  'first_name', 'last_name', 'bio', 'is_private')
        read_only_fields = ['username', 'email']
