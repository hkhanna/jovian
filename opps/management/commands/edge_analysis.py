import json

from django.core.management.base import BaseCommand
from django.conf import settings
from opps.models import User, InterestedIn, Organization, Role


class Command(BaseCommand):
    help = "Analyze the edge cases"

    def handle(self, *args, **options):
        # Load users.json
        users_json = str(settings.BASE_DIR / "opps/json_data/users.json")

        with open(users_json, "r") as f:
            data = json.loads(f.read())

        interested_in = []
        for row in data:
            i = row["interested_in"] or []
            interested_in.extend(i)

        # Load opportunities.json
        opps_json = str(settings.BASE_DIR / "opps/json_data/opportunities.json")

        with open(opps_json, "r") as f:
            data = json.loads(f.read())

        roles = []
        for row in data:
            r = row["roles"] or []
            roles.extend(r)

        interested_in = set(interested_in)
        roles = set(roles)

        print(interested_in.symmetric_difference(roles))
        # {
        #     "Developer I",
        #     "Engineer I",
        #     "Safety Technician I",
        #     "Programmer I",
        #     "Accountant IV",
        #     "Geologist I",
        #     "Budget/Accounting Analyst II",
        # }
