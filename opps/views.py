from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from .models import User, InterestedIn, Organization, Role


class InterestedInSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestedIn
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    interested_in = serializers.SlugRelatedField(
        slug_field="title", many=True, read_only=True
    )

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "interested_in"]


class MatchAPIView(APIView):
    # TODO: deal with auth somehow

    def get(self, request):
        users = User.objects.all()
        data = []
        for user in users:
            serialized = UserSerializer(user).data

            data.append(serialized)

        return Response(data)
