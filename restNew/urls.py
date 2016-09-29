
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken import views as toren_views
from rest_framework import routers
from rest import views

#Routers
router = routers.DefaultRouter()
router.register(r'post_user', views.PostUserList, base_name='posts_user') # Create new post


urlpatterns = [
    url(r'^admin/', admin.site.urls), # admin
    url(r'^token/', toren_views.obtain_auth_token), # get token
    url(r'^', include(router.urls)), # Routers
    url(r'^api-auth', include('rest_framework.urls')),
    url(r'^register/', views.register), # Register
    url(r'^post/create/', views.createpost), # Create Post
    url(r'^posts/', views.PostAllViewSet.as_view()), # List all posts
    url(r'^user/detail/', views.UserDetail.as_view()), # User profile
    url(r'^search/', views.PostSearch.as_view()), # Search

]
