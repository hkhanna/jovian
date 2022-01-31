from django.db import models


class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    first_name = models.CharField(max_length=255, null=False, blank=True)
    last_name = models.CharField(max_length=255, null=False, blank=True)
    email = models.EmailField(max_length=255, null=False, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class InterestedIn(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="interested_in"
    )
    title = models.CharField(max_length=255, null=False, blank=False)


class Organization(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=True)
    email = models.EmailField(max_length=255, null=False, blank=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="roles"
    )
    name = models.CharField(max_length=255, null=False, blank=False)
