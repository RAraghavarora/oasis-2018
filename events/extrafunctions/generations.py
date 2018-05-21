from openpyxl import Workbook
from events.models import *
from preregistration.models import *

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

"""
def RapWarsGeneration(datasheet):
    datasheet["A1"] = "Name"
    datasheet.column_dimensions["A"].width = 20
    datasheet["B1"] = "Rapper Name"
    datasheet.column_dimensions["B"].width = 20
    datasheet["C1"] = "Phone Number"
    datasheet.column_dimensions["C"].width = 15
    datasheet["D1"] = "City"
    datasheet.column_dimensions["D"].width = 10

    event = IntroEvent.objects.get(name="RapWars")

    counter = 2
    for Rapper in
"""
