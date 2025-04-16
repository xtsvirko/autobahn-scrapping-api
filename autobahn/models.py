from django.db import models


# Create your models here.
class Road(models.Model):
    road_id = models.CharField(max_length=20)

    def __repr__(self):
        road_id = self.road_id
        return f"Road({road_id=})"


class Roadwork(models.Model):
    extent = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)
    is_blocked = models.BooleanField()
    title = models.CharField(max_length=255)

    road = models.ForeignKey("Road", on_delete=models.CASCADE, related_name="roadworks")

    def __repr__(self):
        title = self.title
        return f"Roadwork({title=})"
