from django.contrib.admin.views.decorators import staff_member_required
from registrations.models import College

def deepgetattr(obj, attr, default = None):
    
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
        except AttributeError:
            if default:
                return default
            else:
                raise
    return obj

@staff_member_required
def event_list(request, event):

	from django.http import HttpResponse, HttpResponseRedirect, Http404
	import xlsxwriter
	from io import BytesIO

	output = BytesIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet('new-spreadsheet')
	date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})
	worksheet.write(0, 0, "Generated:")
	from time import gmtime, strftime
	generated = strftime("%d-%m-%Y %H:%M:%S UTC", gmtime())
	worksheet.write(0, 1, generated)
	x=2

	try:
		event = MainEvent.objects.get(name=str(event))
	
	except:
		raise Http404("Event name not among : StandUp, Rocktaves, RapWars, StreetDance, PitchPerfect")

	participant_list = IntroReg.objects.filter(event in event_list)

	su_list = [{'obj': i} for i in participant_list]

	if su_list:
		worksheet.write(x, 0, "Required List")
		x+=1
		worksheet.write(x, 0, "S.No.")
		worksheet.write(x, 1, "Name")
		worksheet.write(x, 2, "City")
		worksheet.write(x, 3, "Phone No.")
		worksheet.write(x, 4, "Gender")
		worksheet.write(x, 5, "Email ID")
		x+=1
		for i, row in enumerate(su_list):
			worksheet.write(i+x, 0, i)			
			worksheet.write(i+x, 1, deepgetattr(row['obj'], 'name', 'NA'))
			worksheet.write(i+x, 2, deepgetattr(row['obj'], 'city', 'NA'))
			worksheet.write(i+x, 3, deepgetattr(row['obj'], 'phone', 'NA'))
			worksheet.write(i+x, 4, deepgetattr(row['obj'], 'gender', 'NA'))
			worksheet.write(i+x, 5, deepgetattr(row['obj'], 'email_id', 'NA'))
		x+=len(su_list)+2

	workbook.close()
	filename = 'ExcelReport' + event + '.xlsx'
	output.seek(0)
	response = HttpResponse(output.read(), content_type="application/ms-excel")
	response['Content-Disposition'] = 'attachment; filename=%s' % filename
	return response


@staff_member_required
def college_list(request, pk):

	from django.http import HttpResponse, HttpResponseRedirect, Http404
	import xlsxwriter
	from io import BytesIO

	output = BytesIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet('new-spreadsheet')
	date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})
	worksheet.write(0, 0, "Generated:")
	from time import gmtime, strftime
	generated = strftime("%d-%m-%Y %H:%M:%S UTC", gmtime())
	worksheet.write(0, 1, generated)
	column_no=2

	try:
		college = College.objects.get(pk=pk)
	
	except Exception as e:
		raise Http404('College data does not exist')

	participant_list = college.introreg_set.all()

	su_list = [{'obj': participant} for participant in participant_list]
	if su_list:
		worksheet.write(column_no, 0, "Required List")
		column_no+=1
		worksheet.write(column_no, 0, "S.No.")
		worksheet.write(column_no, 1, "Name")
		worksheet.write(column_no, 2, "City")
		worksheet.write(column_no, 3, "Phone No.")
		worksheet.write(column_no, 4, "Gender")
		worksheet.write(column_no, 5, "Email ID")
		column_no+=1
		for index, row in enumerate(su_list):
			worksheet.write(index+column_no, 0, i)			
			worksheet.write(index+column_no, 1, deepgetattr(row['obj'], 'name', 'NA'))
			worksheet.write(index+column_no, 2, deepgetattr(row['obj'], 'city', 'NA'))
			worksheet.write(index+column_no, 3, deepgetattr(row['obj'], 'phone', 'NA'))
			worksheet.write(index+column_no, 4, deepgetattr(row['obj'], 'gender', 'NA'))
			worksheet.write(index+column_no, 5, deepgetattr(row['obj'], 'email_id', 'NA'))
		column_no+=len(su_list)+2

	workbook.close()
	filename = 'ExcelReport-' + college.name + '.xlsx'
	output.seek(0)
	response = HttpResponse(output.read(), content_type="application/ms-excel")
	response['Content-Disposition'] = 'attachment; filename=%s' % filename
	return response