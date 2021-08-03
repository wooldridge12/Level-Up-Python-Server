from django.db import models


class EventGamer(models.Model):
    event = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    gamer = models.ForeignKey("Event", on_delete=models.CASCADE)