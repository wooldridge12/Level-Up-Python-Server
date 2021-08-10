# """View module for handling requests about park areas"""
# from django.contrib.auth.models import User
# from rest_framework import status
# from rest_framework.decorators import action
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import serializers
# from levelupapi.models import Event, Gamer


# class Profile(ViewSet):

#     def list(self, request):

#         gamer = Gamer.objects.get(user=request.auth.user)
#         events = Event.objects.filter(attendees=gamer)

#         events = EventSerializer(
#             events, many=True, context={'request': request})
#         gamer = GamerSerializer(
#             gamer, many=False, context={'request': request})