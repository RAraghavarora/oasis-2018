from openpyxl import Workbook
from events.models import *
from preregistration.models import *


def RapWarsGeneration(datasheet):
    datasheet["A1"] = "Name"
    datasheet.column_dimensions["A"].width = 20
    datasheet["B1"] = "Rapper Name"
    datasheet.column_dimensions["B"].width = 20
    datasheet["C1"] = "Phone Number"
    datasheet.column_dimensions["C"].width = 15
    datasheet["D1"] = "Email Address"
    datasheet.column_dimensions["D"].width = 30
    datasheet["E1"] = "Gender"
    datasheet.column_dimensions["E"].width = 10
    datasheet["F1"] = "City"
    datasheet.column_dimensions["F"].width = 10
    datasheet["G1"] = "City of Participation"
    datasheet.column_dimensions["G"].width = 20

    counter = 2
    for rapper in RapWarsExtension.objects.all():
        datasheet["A{}".format(counter)] = rapper.participant.name
        datasheet["B{}".format(counter)] = rapper.rapper_name
        datasheet["C{}".format(counter)] = rapper.participant.phone
        datasheet["D{}".format(counter)] = rapper.participant.email_address
        datasheet["E{}".format(counter)] = rapper.participant.gender
        datasheet["F{}".format(counter)] = rapper.participant.city
        datasheet["G{}".format(counter)] = rapper.city_of_participation
        counter += 1

def RocktavesGeneration(datasheet):
    datasheet["A1"] = "Name"
    datasheet.column_dimensions["A"].width = 20
    datasheet["B1"] = "Genre"
    datasheet.column_dimensions["B"].width = 15
    datasheet["C1"] = "Email Address"
    datasheet.column_dimensions["C"].width = 30
    datasheet["D1"] = "Phone Number"
    datasheet.column_dimensions["D"].width = 15
    datasheet["E1"] = "No. of Participants"
    datasheet.column_dimensions["E"].width = 20
    datasheet["F1"] = "Elimination Preference"
    datasheet.column_dimensions["F"].width = 25
    datasheet["G1"] = "Entry 1"
    datasheet.column_dimensions["G"].width = 50
    datasheet["H1"] = "Entry 2"
    datasheet.column_dimensions["H"].width = 50
    datasheet["I1"] = "Other Entries"
    datasheet.column_dimensions["I"].width = 50

    counter = 2
    for Rocktaves in Roctaves.objects.all():
        datasheet["A{}".format(counter)] = Rocktaves.name
        datasheet["B{}".format(counter)] = Rocktaves.genre
        datasheet["C{}".format(counter)] = Rocktaves.email_address
        datasheet["D{}".format(counter)] = Rocktaves.phone
        datasheet["E{}".format(counter)] = Rocktaves.number_of_participants
        datasheet["F{}".format(counter)] = Rocktaves.elimination_preference
        datasheet["G{}".format(counter)] = Rocktaves.entry1
        datasheet["H{}".format(counter)] = Rocktaves.entry2
        datasheet["I{}".format(counter)] = Rocktaves.enteries
        counter += 1

def PurpleProseGeneration(datasheet):
    datasheet["A1"]="Name"
    datasheet.column_dimensions["A"].width = 20
    datasheet["B1"]="College"
    datasheet.column_dimensions["B"].width = 25
    datasheet["C1"]="Phone Number"
    datasheet.column_dimensions["C"].width = 15
    datasheet["D1"]="Email Address"
    datasheet.column_dimensions["D"].width = 20
    datasheet["E1"]="Year and Stream of Study"
    datasheet.column_dimensions["E"].width = 50
    datasheet["F1"]="City of Participation"
    datasheet.column_dimensions["F"].width = 25
    datasheet["G1"]="Entry"
    datasheet.column_dimensions["G"].width = 50

    counter=2
    for prose in PurpleProseExtension.objects.all():
        datasheet["A{}".format(counter)] = prose.participant.name
        datasheet["B{}".format(counter)] = prose.college
        datasheet["C{}".format(counter)] = prose.participant.phone
        datasheet["D{}".format(counter)] = prose.participant.email_address
        datasheet["E{}".format(counter)] = prose.year_and_stream_of_study
        datasheet["F{}".format(counter)] = prose.city_of_participation
        datasheet["G{}".format(counter)] = prose.entry
        counter+=1
    

def StandupSoapboxGeneration(datasheet):
    datasheet["A1"]="Name"
    datasheet.column_dimensions["A"].width = 20
    datasheet["B1"]="Phone Number"
    datasheet.column_dimensions["B"].width = 15
    datasheet["C1"]="Email Address"
    datasheet.column_dimensions["C"].width = 20
    datasheet["D1"]="Doing standup from last(in months)"
    datasheet.column_dimensions["C"].width = 30
    datasheet["E1"]="Previous competitions"
    datasheet.column_dimensions["E"].width = 60
    datasheet["F1"]="City of Participation"
    datasheet.column_dimensions["F"].width = 20

    counter=2

    for soapbox in StandupSoapboxExtension.objects.all():
        datasheet["A{}".format(counter)] = soapbox.participant.name
        datasheet["B{}".format(counter)] = soapbox.participant.phone
        datasheet["C{}".format(counter)] = soapbox.participant.email_address
        datasheet["D{}".format(counter)] = soapbox.time_doing_standup
        datasheet["E{}".format(counter)] = soapbox.previous_competition
        datasheet["F{}".format(counter)] = soapbox.city_of_participation
        counter+=1
        
           
    
    
    