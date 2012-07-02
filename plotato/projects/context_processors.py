from django.conf import settings

def site_name(context):
	return {'SITE_NAME' : settings.SITE_NAME}