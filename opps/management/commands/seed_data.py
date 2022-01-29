import json

from django.core.management.base import BaseCommand
from django.conf import settings
from opps.models import User, InterestedIn, Organization, Role


class Command(BaseCommand):
    help = "Load users.json and opportunities.json into database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete all users and opportunities first",
        )

    def handle(self, *args, **options):
        if options["delete"]:
            User.objects.all().delete()
            Organization.objects.all().delete()

        # Load users.json
        users_json = str(settings.BASE_DIR / "opps/json_data/users.json")

        with open(users_json, "r") as f:
            data = json.loads(f.read())

        users = []
        interests = []
        for row in data:
            user = User(
                id=row["id"],  # If there's no ID, it should error.
                first_name=row.get("first_name", "")
                or "",  # Edge case: dealing with nulls
                last_name=row.get("last_name", "")
                or "",  # Edge case: dealing with nulls
                email=row.get("email", "") or "",  # Edge case: dealing with nulls
            )
            users.append(user)

            interested_in = (
                row.get("interested_in") or []
            )  # Edge case: dealing with nulls
            interests.extend([InterestedIn(user=user, title=i) for i in interested_in])

        User.objects.bulk_create(users)
        InterestedIn.objects.bulk_create(interests)
        print("users.json ingested")

        # Load opportunities.json
        opps_json = str(settings.BASE_DIR / "opps/json_data/opportunities.json")

        with open(opps_json, "r") as f:
            data = json.loads(f.read())

        orgs = []
        roles = []
        for row in data:
            org = Organization(
                id=row["id"],  # If there's no ID, it should error.
                name=row.get("organization", "") or "",  # Edge case: dealing with nulls
                email=row.get("email", "") or "",  # Edge case: dealing with nulls
            )
            orgs.append(org)

            roles_json = row.get("roles") or []  # Edge case: dealing with nulls
            roles.extend([Role(organization=org, name=r) for r in roles_json])

        Organization.objects.bulk_create(orgs)
        Role.objects.bulk_create(roles)
        print("opportunities.json ingested")
