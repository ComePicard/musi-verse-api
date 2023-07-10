"""
URL configuration for API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from api_musi.user.views import CreateUserAPIView
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,

)

import article.views

import user.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/', user.views.UserAPI.as_view(), name='create_user / get'),
    path('users/<str:username>/', user.views.GetUserByUsername.as_view(), name='user'),
    path('moderators/', user.views.ModeratorMembersView.as_view(), name='get_mods'),
    path('moderators/add/', user.views.ModeartorAdd.as_view(), name='mode_add'),
    path('moderators/remove/', user.views.ModeartorRemove.as_view(), name='mod_rem'),
    path('articles/image/', article.views.UploadImageToArticle.as_view()),
    path('articles/verify/', article.views.ArticleModView.as_view()),
    path('articles/', article.views.ArticleAPIView.as_view()),
    path('articles/<str:route>', article.views.ArticleNamesAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('attributes/', article.views.CreateAttribute.as_view()),
    path('attributes/set/', article.views.SetAttribute.as_view()),
    path('attributes/vote/', article.views.AttributeVoteAPIView.as_view()),
    path('attributes/<int:attribute_id>/', article.views.SetAttribute.as_view(), name='delete-attribute'),
    path('articles/<str:route>/comments/',article.views.CommentDetailView.as_view(), name='comment-detail'),
    path('articles/<str:route>/comments/vote/', article.views.CommentVoteAPIView.as_view(), name='comment-vote'),


]

