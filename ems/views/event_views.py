from django.contrib.auth.models import User
from django.shortcuts import render, reverse

from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from events.models import MainEvent
from ems.models.level import LevelClass, LevelInstance
from ems.permissions import IsClubDept
from ems.serializers import *

class LevelList(APIView):

	#permission_classes = (IsAuthenticated, IsClubDept)
	parser_classes = (FormParser, JSONParser, MultiPartParser)
	renderer_classes = (TemplateHTMLRenderer,)

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
				'url':request.build_absolute_uri(reverse('ems:index'))
			}			
			return Response(context, template_name = "registrations/message.html")
		
		levels = LevelClass.objects.filter(event = event)		
		context = {"event" : event, "levels" : levels}
		return Response(context, template_name = "ems/event_levels.html")

	def post(self, request, event_id):
		if data['action'] == 'delete':
			try:
				parts_id = data.getlist('level_ids')
			except:
				return redirect(request.META.get('HTTP_REFERER'))
			
			for pk in level_ids:
				try:
					level = LevelClass.objects.get(id = pk)
				
				except:
					context = {
						'error_heading':'Error Occured',
						'message':'Sorry, you cannot perform this action',
						'url':request.build_absolute_uri(reverse('registrations:home'))
					}
					return render(request, 'registrations/message.html', context)
				
				level.teams.clear()
				level.delete()

		elif data['action'] == 'add':
			data = request.POST
			try:
				name = data['name']
				if name == '':
					raise Exception
				names = data['parameters'].split('?')
				maxes = list(map(lambda x: int(x.strip()), data['values'].split('?')))
				if not len(names) == len(maxes):
					raise Exception
			except:
				messages.warning(request, 'Please Fill the details of the level properly')
			return redirect(request.META.get('HTTP_REFERER'))

			level = Level.objects.create(name=name, position=position+1, event=event)
			for i, n in enumerate(names):
				p=Parameter.objects.create(name=n, max_val=int(maxes[i]), level=level)
			for team in Team.objects.filter(event=event):
				for s in team.scores.all():
					s.save()
			return redirect(reverse_lazy('ems:event_levels', kwargs={'e_id':event.id}))
		
			

class LevelDetail(APIView):

	#permission_classes = (IsAuthenticated, IsClubDept)
	parser_classes = (FormParser, JSONParser, MultiPartParser)
	renderer_classes = (TemplateHTMLRenderer,) 

	def get(self, request, level_id):
		try:
			level = LevelClass.objects.get(pk = level_id)
		except:
			context = {
				'error_heading': "Error",
				'message': "Level does not exist.",
				'url':request.build_absolute_uri(reverse('ems:index'))
			}			
			return Response(context, template_name = "registrations/message.html")
    	
		params = level.parameters.all()
		context = {
			"event" : level.event, 
			"level" : level,
			"params" : level.parameters.all(),
			"return" : request.META.get('HTTP_REFERER'),
    		"param_str" : '?'.join([param.name for param in params]),
    		"max_str" : '?'.join([str(param.max_value) for param in params])
		}

		return Response(context, template_name = "ems/show_level.html")		

	def post(self, request, level_id):
		pass
		# level = Level.objects.get(id=data['level_id_update'])
  #       level.name = name
  #       level.save()
  #       params = level.parameter_set.all()
  #       params.delete()