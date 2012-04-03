plotato
=====

*Please note that plotato is not currently in a stage intended for online use.*

plotato is a django 1.3.1 web application for presenting user defined plots. It uses the bootstrap from Twitter (http://twitter.github.com/bootstrap/).

For data access and manipulation it provides a REST API for data management and it uses matplotlib for plotting.

To get started follow the guide below, but please note that the guide is only tested on Linux. It should however work on both windows and mac too without too much hassle.

How to Get Started
=====
  * sudo apt-get install python pip virtualenv
  * Download and extract project
  * Go into the directory and run the following commands
  * virtualenv .
  * source bin/activate
  * pip install hg+https://bitbucket.org/wkornewald/django-nonrel
  * pip install hg+https://bitbucket.org/wkornewald/djangotoolbox
  * pip install git+https://github.com/django-nonrel/mongodb-engine
  * pip install django-tastypie
  * pip install git+https://github.com/andresdouglas/django-tastypie-nonrel.git
  * pip install numpy
  * pip install matplotlib
  * setup a mongodb server, see http://www.mongodb.org/display/DOCS/Quickstart
  * ./manage syncdb
  * ./manage runserver 8080
  * Open your browser and goto http://localhost:8080/
  * You should now see plotato running, and you can freely add projects tests and plots.
  * Note: Runs are added via the tasty pie rest API.
  * If you want to see examples of how to get and retrieve data via the tastypie rest API look in the tools folder.
  * Enjoy!