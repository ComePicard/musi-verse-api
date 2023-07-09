from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import Group

def is_user_mod(user):
    moderator_group = Group.objects.get(name='Moderator')
    return user.groups.filter(name=moderator_group).exists()
