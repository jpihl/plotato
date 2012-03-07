Plotato
=====

*Please note that plotato is not currently in a stage intented for online use.*

Plotato is a django 1.3.1 web application for presenting user defined plots. It uses the boostrap from Twitter (http://twitter.github.com/bootstrap/).

It provides a REST API for data management and it uses mathplotlib for plotting.

Dependencies:
  * django.contrib.admin
  * djangorestframework (http://django-rest-framework.org)

These needs to be added to INSTALLED_APPS in your settings.py file.

How to get started
=====
  * Install django.
  * Install djangorestframework.
  * Start a django project using the folloing command: "django-admin.py startproject plotato" ("plotato" or whatever you like..).
  * Download the plotato source and place it in the same folder as the newly created project.
  * Fill in your configuration in the settings.py file add the following to your INSTALLED_APPS: "django.contrib.admin, djangorestframework, dataman, projects, projects.plots".
  * Now sync the database using the following command "./manage.py syncdb", and start the server using "./manage.py runserver [DESIRED_PORT]".