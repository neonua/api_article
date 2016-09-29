# -*- coding: utf-8 -*-

from models import Post
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework import status, serializers, permissions


UserModel = get_user_model() # Get user model


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create(
            email=validated_data['email'],
            firstname = validated_data['firstname'],
            lastname = validated_data['lastname']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = UserModel

class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny, # Or anon users can't register
    ]
    serializer_class = UserRegisterSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserModel
        fields = ('email', 'firstname', 'lastname')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'body', 'user_id')


class PostCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        article = Post(
            title=validated_data['title'],
            body=validated_data['body'],
        )
        return article

    class Meta:
        model = Post
        fields = ('title', 'body')

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post