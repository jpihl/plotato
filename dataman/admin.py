from dataman.models import DataSet, DataEntry
from django.contrib import admin

class DataEntryInLine(admin.TabularInline):
	model = DataEntry
	extra = 10

class DataSetAdmin(admin.ModelAdmin):
	fielsets = [
		(None, {'fields':['name']}),
		(None, {'fields':['unit']}),
		('Description', {'fields':['desc'], 'classes': ['collapse']}),
		(None,			{'fields':['project'], 'classes': ['collapse']}),
		
	]
	inlines = [DataEntryInLine]

admin.site.register(DataSet, DataSetAdmin)