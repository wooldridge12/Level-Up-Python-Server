from django.db import models


class Event(models.Model):
    host = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    game = models.Foreignkey("Game", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    attendees = models.ManyToManyField("Gamer", through="EventGamer", related_name="attending")
    