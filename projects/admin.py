from projects.models import Project
from django.contrib import admin

class ProjectAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields':['name']}),
		(None, {'fields':['description']}),
	]

admin.site.register(Project, ProjectAdmin)


