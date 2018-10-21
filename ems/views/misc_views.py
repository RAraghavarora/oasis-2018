from django.contrib.auth import logout
from django.shortcuts import redirect, reverse
from django.core.urlresolvers import reverse_lazy

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer


from ems.models.clubdept import ClubDepartment 


class Index(APIView):

    permission_classes = (IsAuthenticated,)
    renderer_classes = (TemplateHTMLRenderer,)


    def get(self, request):
        user = request.user

        # if user.is_superuser or user.username=='controls':
        #     return redirect(reverse_lazy('ems:events_controls'))

        # try:
        #     judge = user.judge
        #     return redirect(reverse('ems:update_scores', kwargs={'level_id':judge.level.id}))
        # except:
        #     pass

        # try:
        #     clubdept = ClubDepartment.objects.get(user = user)
        #     return redirect('ems:events_select')
        # except:
        #     pass

        # logout(request)
        # return redirect(reverse_lazy('ems:login'))    
        return Response(template_name = 'ems/add_level.html')