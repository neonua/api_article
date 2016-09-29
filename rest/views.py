# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest.serializers import UserSerializer, PostSerializer, PostCreateSerializer, UserRegisterSerializer
from models import Post
from rest_framework.pagination import PageNumberPagination

# Create your views here.

UserModel = get_user_model()

# My pagination from articles full list
class Pagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

# Registration user
@api_view(['POST']) # Only Post
@permission_classes((AllowAny,)) # Permissions from all
def register(request):
    serialized = UserRegisterSerializer(data=request.data)
    if serialized.is_valid():
        # if firstname
        if 'firstname' in serialized.initial_data:
            firstname = serialized.initial_data['firstname']
        else:
            firstname = None

        # if lastname
        if 'lastname' in serialized.initial_data:
            lastname = serialized.initial_data['lastname']
        else:
            lastname = None
        user = UserModel(
            email = serialized.initial_data['email'],
            firstname = firstname,
            lastname = lastname,
        )
        user.set_password(serialized.initial_data['password']) # using sha-256
        user.save()
        return Response('ok:) Now try to get token!')
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


# class UserViewSet(viewsets.ModelViewSet):
#
#     queryset = UserModel.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer


# Get all articles
class PostAllViewSet(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = Pagination

# Create POST
@api_view(['POST']) # only POST
def createpost(request):
    serialized = PostCreateSerializer(data=request.data)
    if serialized.is_valid():
        article = Post(
            title=serialized.initial_data['title'],
            body=serialized.initial_data['body'],
            user_id=request.user
        )
        article.save()

        return Response('{0}create!'.format(serialized.initial_data['title'],))
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


# Users Articles
class PostUserList(viewsets.ViewSet):

    pagination_class = Pagination # using my paginator
    def list(self, request):
        queryset = Post.objects.filter(user_id=request.user)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

# Search
class PostSearch(ListAPIView):
    serializer_class = PostSerializer

    def list(self, request):
        queryset = Post.objects.filter(title=self.request.query_params['search']) # get params search
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

# Profile user
class UserDetail(ListAPIView):
    serializer_class = UserSerializer

    def list(self, request):

        queryset = UserModel.objects.get(email=self.request.user)
        serializer = UserSerializer(queryset, many=False)
        return Response(serializer.data)
