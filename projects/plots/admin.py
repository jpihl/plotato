from projects.plots.models import Plot
from django.contrib import admin

class PlotAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields':['name']}),
		(None, {'fields':['code']}),
		(None, {'fields':['project']}),
	]

admin.site.register(Plot, PlotAdmin)