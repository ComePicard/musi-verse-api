import permission as permission
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserSerializer


class UserAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        try:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=404)


class GetUserByUsername(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=404)


class ModeratorMembersView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        moderator_group = Group.objects.get(name='Moderator')

        members = User.objects.filter(groups=moderator_group)
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)


class ModeartorAdd(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def patch(self, request):
        moderator_group = Group.objects.get(name='Moderator')
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        user.groups.add(moderator_group)

        return Response({'message': 'Role "Moderator" assigned successfully.'})


class ModeartorRemove(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def patch(self, request):
        moderator_group = Group.objects.get(name='Moderator')
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        user.groups.remove(moderator_group)
        return Response({'message': 'Role "Moderator" removed successfully.'})
