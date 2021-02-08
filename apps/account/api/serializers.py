from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from apps.account.models import User
from rest_framework_jwt.serializers import jwt_payload_handler, \
    jwt_encode_handler
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.message import EmailMessage
from django.template import loader
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import serializers


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name',)
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'],
                                   first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={"blank": "Este campo es obligatorio"})
    password = serializers.CharField(
        error_messages={"blank": "Este campo es obligatorio"})

    def validate(self, attrs):
        self.user_cache = authenticate(email=attrs["email"],
                                       password=attrs["password"])
        if not self.user_cache:
            raise serializers.ValidationError("Invalid login")
        else:
            payload = jwt_payload_handler(self.user_cache)

            return {
                'token': jwt_encode_handler(payload),
                'user': self.user_cache
            }

    def get_user(self):
        return self.user_cache


class RetrieveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',)
        read_only_fields = ('id', 'email',)


class EmailContactSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True)

    def send_mail(self, random):
        send_mail(
            '{} want to contact us! '.format(self.validated_data["full_name"]),
            '''
            Fullname: {}
            Email: {}
            Random: {}
            Cellphone: 987654321
            Message: Esto es un mensaje de prueba sin asincronía
            '''.format(self.validated_data["full_name"],
                       random,
                       self.validated_data["email"]),
            self.validated_data.get("email"),
            ['richard.cancino@securitec.pe'],
            fail_silently=False)
