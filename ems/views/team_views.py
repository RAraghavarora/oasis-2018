from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser



from registrations.models import MainEvent
from ems.models.team import Team

from ems.serializers import TeamSerializer

class TeamList(APIView):

	# permission_classes = (IsAuthenticated)
	renderer_classes = (TemplateHTMLRenderer,JSONRenderer)
	parser_classes = (FormParser,JSONParser, MultiPartParser)


	def get(self, request, event_id):
		try:
			event = MainEvent.objects.get(id = event_id)
		except MainEvent.DoesNotExist:
			context = {
				'error_heading': "Error",
				'message': "Event does not exist",
				'url':request.build_absolute_uri(reverse('ems:index'))
				}
			return Response(context, template_name='registrations/message.html')
		print(event)
		teams = Team.objects.filter(event = event)
		#serializer = TeamSerializer(teams, many = True)

		response = {
			"event" : event,
			"teams" : teams
		}

		return Response(response, template_name = 'ems/team_details_home.html', status = status.HTTP_200_OK)


	def post(self, request, event_id):
		try:
			event = MainEvent.objects.get(id = event_id)
		except Event.DoesNotExist:
			msg = {"message" : "Event with the following id doesn't exist: {}".format(event_id)}
			return Response(msg, status = status.HTTP_404_NOT_FOUND)

		data = request.data
		if data['submit']=='delete_teams':
			print('yes')

		serializer = TeamSerializer(data = req)

class TeamDetail(APIView):

	# permission_classes = (IsAuthenticated)

	def get(self, request, team_id):
		try:
			team = Team.objects.get(id = team_id)
		except Team.DoesNotExist:
			msg = {"mesage" : "Team doesn't exist"}
			return Response(msg, status = status.HTTP_404_NOT_FOUND)

		serializer = TeamSerializer(team)

		return Response(serializer.data, status = status.HTTP_200_OK)

	def post(self, request, team_id):
		pass