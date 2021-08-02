from django.db import Model 


class EventGamer():
    event = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    gamer = models.ForeignKey("Event", on_delete=models.CASCADE)