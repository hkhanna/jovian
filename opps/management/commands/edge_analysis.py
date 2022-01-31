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

        # Interesting that there's differences that would be solved by stemming. Maybe lemmetization, but
        # unclear whether that would work. Not enough time to experiment.
        # Edge cases: Software Engineer <-> Developer <-> Programmer
        # Edge case: Engineer could be any kind of engineer, so we only match with other bare Engineer.
        # Edge case: Roman numeral
        # Edge case: Roman numeral: None specified -> Any
        # Edge case: split slashes
        # Edge case: Assistant <-> Analyst
        # Stretch -- more robust: Vectorize all the words in the corpus and calculate the cosine similarity or L2 normalized distance to each other.
        #   To be overinclusive, probably would compare each word individually and report any thing that passed the cutoff.
        #   Stricter approach would be to compare every word and report where more than X% passed the cutoff.
        #   Could also get fancy and use more modern "sentence" comparison techniques like WMD (word mover distance).
        #   Could train my own embeddings based on past matches. Lots of directions we could go.
