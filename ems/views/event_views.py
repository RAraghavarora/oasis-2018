from django.contrib.auth.models import User
from django.shortcuts import render, reverse

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import MainEvent
from ems.models.level import LevelClass, LevelInstance
from ems.permissions import IsClubDept
from ems.serializers import *

class LevelList(APIView):

	permission_classes = (IsAuthenticated,IsClubDept)

	def get(self, request, event_id):
		'''
		Will display all the levels of the event along with the option to add a new level.
		'''
		try:
			event = MainEvent.objects.get(pk = event_id)
		except:
			context = {
			'error_heading': "Error",
			'message': "Event does not exist.",
			'url':request.build_absolute_uri(reverse('regsoft:firewallz_home'))
			}
			return render(request, 'registrations/message.html', context)
		levels = LevelClass.objects.filter(event = event)
		serializer = LevelClassSerializer(levels, many = True)
		return Response(serializer.data, status = status.HTTP_200_OK)


class LevelDetail(APIView):

	permission_classes = (IsAuthenticated, IsClubDept)

	def get(self, request, event_id):
		pass

	def post(self, request, event_id):
		pass

	def delete(self, request, event_id):
		pass