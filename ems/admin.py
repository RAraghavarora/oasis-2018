from django.contrib import admin

from ems.models.clubdept import ClubDepartment
from ems.models.judge import Judge
from ems.models.level import LevelClass, LevelInstance
from ems.models.parameter import ParameterClass, ParameterInstance 
from ems.models.team import Team


class LevelInstanceInLine(admin.TabularInline):
    model = LevelInstance
    extra = 1


class LevelClassAdmin(admin.ModelAdmin):
    inlines = [LevelInstanceInLine]


class ParameterInstanceInLine(admin.TabularInline):
    model = ParameterInstance
    extra = 1


class ParameterClassAdmin(admin.ModelAdmin):
    inlines = [ParameterInstanceInLine]


admin.site.register(ClubDepartment)
admin.site.register(Team)
admin.site.register(Judge)
admin.site.register(LevelClass, LevelClassAdmin)
admin.site.register(LevelInstance)
admin.site.register(ParameterClass, ParameterClassAdmin)
admin.site.register(ParameterInstance)