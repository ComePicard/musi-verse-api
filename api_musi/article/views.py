import rest_framework.views
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Article, Image, Attribute, ArticleAttribute

import json

class ArticleNamesAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, route):
        article = Article.objects.get(route=route)
        article.views += 1
        article.save()
        article_dict = model_to_dict(article)
        return Response(article_dict)


class ArticleAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        # TODO: Perform data validation

        new_article = Article(
            name=data['name'],
            categories=data['categories'],
            description=data['description'],
            price_range=data['price_range'],
            route=data['name'].strip().replace(" ", "_").lower(),
            author=request.user
        )
        new_article.save()
        return Response(f"Article {data['name']} created")
    def get(self, request):
        articles = Article.objects.all()
        result = []

        for article in articles:
            attrs = ArticleAttribute.objects.all().filter(article=article.id)
            print(attrs)
            temp = []
            for attr in attrs:
                print(attrs)
                temp.append(model_to_dict(attr))
            result.append([model_to_dict(article),temp])
        return Response(result)



class UploadImageToArticle(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        data = request.data
        #TODO data valid
        if True:
            new_image = Image()
            new_image.name = data['name']
            new_image.image = request.FILES['image']
            new_image.description = data['descritpion']
            new_image.author = request.user
            new_image.article = Article.objects.get(id=data['article'])
            new_image.save()
            return Response(f"Image {data['name']} was uploaded")

class CreateAttribute(APIView):
    def post(self, request):
        try :
            attribute = Attribute()
            attribute.content = request.data['content']
            attribute.save()
            return Response('Added ' + request.data['content'] , status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response('Already exists',status=status.HTTP_409_CONFLICT)

    def get(self,request):
        attributes = Attribute.objects.all()
        temp = []
        for attr in attributes:
            temp.append(model_to_dict(attr))
        return Response(temp)

class SetAttribute(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        try :
            art_attribute = ArticleAttribute()
            art_attribute.attr = Attribute.objects.get(id=request.data['attr'])
            art_attribute.attribute_type = request.data['attribute_type']
            art_attribute.article = Article.objects.get(id=request.data['id_article'])
            art_attribute.save()
            return Response('Added ' + request.data['attr'] , status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(e)

    def get(self,request):
        attributes = ArticleAttribute.objects.all()
        temp = []
        for attr in attributes:
            temp.append(model_to_dict(attr))
        return Response(temp)