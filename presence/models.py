import json
from django.db import models


class Presence(models.Model):
    username = models.CharField(max_length=10, blank=False, null=False)

    def to_json(self):
        return json.dumps({"username": self.username})

    def get_presence_items():
        """
        Queries the database for all of the presence objects
        Returns a list of json serialized objects
        """
        return list(map(lambda x: x.to_json(), Presence.objects.all()))
