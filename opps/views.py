import re
from collections import defaultdict
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework import serializers
from .models import User, Role


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

        # Search user interests
        search = request.GET.get("search")
        if search:
            user_qs = user_qs.filter(interested_in__title__icontains=search)

        # Pagination
        user_qs = self.paginator.paginate_queryset(user_qs, request, view=self)

        data = []
        for user in user_qs:
            serialized = UserSerializer(user).data
            matches = []
            for i in serialized["interested_in"]:
                # If there was a search, remove all non-matching interests.
                if search and search.lower() in i.lower():
                    matches.append(roles[i])
                elif not search:
                    matches.append(roles[i])
            serialized["matches"] = matches
            data.append(serialized)

        return self.paginator.get_paginated_response(data)

    @staticmethod
    def _get_variations(name):
        """Deal with edge cases by reporting other possible names"""

        # Exact match
        variants = [name]

        # Edge case: Software Engineer <-> Developer <-> Programmer
        name_derived = re.sub("Software Engineer", "Developer", name)
        variants.append(name_derived)
        name_derived = re.sub("Software Engineer", "Developer", name)
        variants.append(name_derived)

        name_derived = re.sub("Developer", "Software Engineer", name)
        variants.append(name_derived)
        name_derived = re.sub("Developer", "Programmer", name)
        variants.append(name_derived)

        name_derived = re.sub("Programmer", "Software Engineer", name)
        variants.append(name_derived)
        name_derived = re.sub("Programmer", "Developer", name)

        # Edge case: Allow some squishiness on the level (+/- 1 level)
        tokens = name.split()
        numeral = tokens[-1]
        if numeral in ROMAN_TO_ARABIC.keys():
            arabic = ROMAN_TO_ARABIC[numeral]
            lower = arabic - 1
            higher = arabic + 1
            if lower in ARABIC_TO_ROMAN.keys():
                tokens[-1] = ARABIC_TO_ROMAN[lower]
                name_derived = " ".join(tokens)
                variants.append(name_derived)
            if higher in ARABIC_TO_ROMAN.keys():
                tokens[-1] = ARABIC_TO_ROMAN[higher]
                name_derived = " ".join(tokens)
                variants.append(name_derived)

        # Possible improvements:
        #  - Combine all the variants with each other (although this could quickly get unmanagable depending on the number of edge cases we handle)
        #  - Compare on individual words to catch things like VP Accounting -> Accounting Analyst V

        return set(variants)


ROMAN_TO_ARABIC = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "IX": 9,
    "X": 10,
}
ARABIC_TO_ROMAN = {v: k for k, v in ROMAN_TO_ARABIC.items()}
