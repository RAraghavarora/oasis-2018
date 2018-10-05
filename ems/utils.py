def determine_identity(user):
	if user.is_authenticated():
        if user.is_superuser or user.username == 'controls':
            ret_string = {
            	"identity" : "super"
            }
            return ret_string
        try:
            judge = user.judge
            ret_string = {
            	"identity" : "judge",
            	"judge" : judge
            }
            return ret_string
        except:
            pass
        try:
            clubdept = ClubDepartment.objects.get(user=request.user)
            ret_string = {
            	"identity" : "clubdept",
            	"clubdept" : clubdept
            }
            return ret_string            
            return redirect('ems:events_select')
        except:
            pass