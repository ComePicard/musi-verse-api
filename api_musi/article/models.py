from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.


class Article(models.Model):
    class Meta:
        app_label = 'article'
    name = models.CharField(default=['ArticleDefault'], max_length=200,unique=True)
    CORDES_PINCEES = "Cordes pincées"
    CORDES_FROTTEES = "Cordes frottées"
    VENTS = "Vents"
    PERCUSSIONS = "Percussions"
    AUTRE = "Autre"

    INSTRUMENT_CATEGORIES = [
        (CORDES_PINCEES, "Cordes pincées"),
        (CORDES_FROTTEES, "Cordes frottées"),
        (VENTS, "Vents"),
        (PERCUSSIONS, "Percussions"),
        (AUTRE, "Autre"),
    ]
    categories = models.CharField(
        max_length=40,
        choices=INSTRUMENT_CATEGORIES,
        default=AUTRE,
    )
    description = models.TextField(max_length=10000,
                                   default="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
    price_range = ArrayField(
        models.FloatField(max_length=25, blank=True),
        size=2,
        default=list
    )
    creation_date = models.DateTimeField(db_comment="Date and time when the article was published", auto_now_add=True)
    last_update = models.DateTimeField(db_comment="Last Update", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    route = models.CharField(default=['route'], max_length=200,unique=True)
    views = models.PositiveIntegerField(default=0)



class Image(models.Model):
    class Meta:
        app_label = 'article'
    image = models.ImageField(upload_to="./images/instruments")
    name = models.CharField(default=['ImageDefault'], max_length=200, unique=True)
    description = models.TextField(max_length=10000,
                                   default="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")


    creation_date = models.DateTimeField(db_comment="Date and time when the image was published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, default=None)

class Attribute(models.Model):
    class Meta:
        app_label = 'article'

    content = models.TextField(unique=True)

class ArticleAttribute(models.Model):
    ATTRIBUTE_CHOICES = [
        ('pros', 'Pros'),
        ('cons', 'Cons'),
    ]

    attr = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    attribute_type = models.CharField(max_length=4, choices=ATTRIBUTE_CHOICES)

    class Meta:
        app_label = 'article'


class AttributeNote(models.Model):
    article_attribute = models.ForeignKey(ArticleAttribute, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.upvote and self.downvote:
            self.upvote = False
        elif not self.upvote and not self.downvote:
            self.downvote = False

        super().save(*args, **kwargs)