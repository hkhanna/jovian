from collections import defaultdict
from email.policy import default
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from .models import User, InterestedIn, Organization, Role


class UserSerializer(serializers.ModelSerializer):
    interested_in = serializers.SlugRelatedField(
        slug_field="title", many=True, read_only=True
    )

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "interested_in"]


class RoleSerializer(serializers.Serializer):
    role_name = serializers.CharField(source="name", read_only=True)
    organization_name = serializers.CharField(
        source="organization.name", read_only=True
    )
    organization_email = serializers.EmailField(
        source="organization.email", read_only=True
    )


class MatchAPIView(APIView):
    paginator = LimitOffsetPagination()

    def get(self, request):
        role_qs = Role.objects.select_related("organization").all()

        # Hash table reduces the time complexity of what would be O(n^2) in the naive solution.
        # Should be O(n) now.
        roles = defaultdict(list)
        for role in role_qs:
            serialized = RoleSerializer(role).data

            rolename_variations = self._get_variations(role.name)
            for name in rolename_variations:
                roles[name].append(serialized)

        user_qs = User.objects.prefetch_related("interested_in")
        user_qs = self.paginator.paginate_queryset(user_qs, request, view=self)
        data = []
        for user in user_qs:
            serialized = UserSerializer(user).data
            matches = []
            for i in serialized["interested_in"]:
                matches.append(roles[i])
            serialized["matches"] = matches
            data.append(serialized)

        return self.paginator.get_paginated_response(data)

    @staticmethod
    def _get_variations(name):
        return [name]
