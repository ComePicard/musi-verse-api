import rest_framework.views
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Image

import json

class ArticleNamesAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        articles = Article.objects.all().values('name', 'categories', 'route')
        result = []
        for article in articles:
            result.append({
                'name': article['name'],
                'value': article['categories'],
                'route': article['route']
            })
        return Response(result)

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

    def get(self, request, route):
        article = Article.objects.get(route=route)
        article.views += 1
        article.save()
        article_dict = model_to_dict(article)
        return Response(article_dict)


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


