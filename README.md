# Plotato Django Project #
Plotato is a django 1.4 web application for storing data and presenting it with customizable plots.

## Prerequisites ##

- python >= 2.7
- pip
- virtualenv/wrapper (optional)

## Installation ##
### Creating the environment ###
Create a virtual python environment for the project.
If you're not using virtualenv you may skip this step.

#### For virtualenv ####
```bash
virtualenv --no-site-packages plotato-env
cd plotato-env
source bin/activate
```

### Clone the code ###
Obtain the url to your git repository.

```bash
git clone git://github.com/jpihl/plotato.git plotato
git submodule init
git submodule update
```

### Install requirements ###
```bash
cd plotato
pip install numpy
pip install matplotlib
pip install -r requirements.txt
```

### Configure project ###
```bash
cp plotato/__local_settings.py plotato/local_settings.py
vi plotato/local_settings.py
```

### Sync database ###
```bash
python manage.py syncdb
```

## Running ##
```bash
python manage.py runserver
```

Open browser to http://127.0.0.1:8000
