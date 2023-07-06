import rest_framework.views
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Article, Image, Attribute, ArticleAttribute, AttributeNote

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

            article_attributes = []
            for art_attr in attrs:
                attrs_vote = AttributeNote.objects.all().filter(article_attribute=art_attr.id)
                total_upvotes = AttributeNote.objects.filter(article_attribute=art_attr.id, upvote=True).count()
                total_downvotes = AttributeNote.objects.filter(article_attribute=art_attr.id, downvote=True).count()

                article_attributes.append({"attribute_name": Attribute.objects.get(id=art_attr.attr.id).content,
                                           "article_attribute": model_to_dict(art_attr),
                                           "article_votes": {"downvotes": total_downvotes,
                                                             "upvotes": total_upvotes}})

            result.append([model_to_dict(article), article_attributes])
        return Response(result)


class UploadImageToArticle(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data = request.data
        # TODO data valid
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
        try:
            attribute = Attribute()
            attribute.content = request.data['content']
            attribute.save()
            return Response('Added ' + request.data['content'], status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response('Already exists', status=status.HTTP_409_CONFLICT)

    def get(self, request):
        attributes = Attribute.objects.all()
        temp = []
        for attr in attributes:
            temp.append(model_to_dict(attr))
        return Response(temp)


class SetAttribute(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:

            art_attribute = ArticleAttribute()
            art_attribute.attr = Attribute.objects.get(id=request.data['attr'])
            art_attribute.attribute_type = request.data['attribute_type']
            art_attribute.article = Article.objects.get(id=request.data['id_article'])
            art_attribute.save()
            return Response('Added ' + request.data['attr'], status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(e)

    def get(self, request):
        attributes = ArticleAttribute.objects.all()
        temp = []
        for attr in attributes:
            temp.append(model_to_dict(attr))
        return Response(temp)

    def delete(self, request, attribute_id):
        try:
            art_attribute = ArticleAttribute.objects.get(id=attribute_id)
            total_upvotes = AttributeNote.objects.filter(article_attribute=art_attribute.id, upvote=True).count()
            total_downvotes = AttributeNote.objects.filter(article_attribute=art_attribute.id, downvote=True).count()
            if art_attribute.user == request.user and total_downvotes+total_downvotes < 3:
                art_attribute.delete()
                return Response('Attribute deleted successfully', status=status.HTTP_200_OK)
        except ArticleAttribute.DoesNotExist:
                return Response('Attribute not found', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
                print(e)
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class AttributeVoteAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        art_attribute_id = request.data.get('art_attribute_id')
        vote_type = request.data.get('vote_type')  # 'upvote' or 'downvote'
        art_attribute = ArticleAttribute.objects.get(id=art_attribute_id)

        try:
            attribute_note = AttributeNote.objects.get(article_attribute=art_attribute, user=request.user)

            # Check if the current vote type matches the existing vote
            if vote_type == 'upvote' and attribute_note.upvote:
                # Resending an upvote, set it to False
                attribute_note.upvote = False
            elif vote_type == 'downvote' and attribute_note.downvote:
                # Resending a downvote, set it to False
                attribute_note.downvote = False
            else:
                # Update the vote fields based on the vote_type
                attribute_note.upvote = vote_type == 'upvote'
                attribute_note.downvote = vote_type == 'downvote'

        except AttributeNote.DoesNotExist:
            # Create a new AttributeNote instance if none exists
            attribute_note = AttributeNote(article_attribute=art_attribute, user=request.user)
            attribute_note.upvote = vote_type == 'upvote'
            attribute_note.downvote = vote_type == 'downvote'

        attribute_note.save()

        return Response({'message': 'Vote recorded successfully.'})
