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

#### For Virtualenv (optional) ####
```bash
virtualenv --no-site-packages plotato-env
cd plotato-env
source bin/activate
```

### Clone the Code ###
Obtain the url to your git repository.

```bash
git clone git://github.com/jpihl/plotato.git plotato
cd plotato
git submodule init
git submodule update
```

### Install Requirements ###
```bash
pip install numpy
pip install -r requirements.txt
```

### Configure Project ###
```bash
cp plotato/__local_settings.py plotato/local_settings.py
vi plotato/local_settings.py
```

### Sync Database ###
```bash
python manage.py syncdb
```

### Load Sample Data (optional) ###
```bash
python manage.py loaddata plotato/fixtures/sample_data.json
```

## Running ##
```bash
python manage.py runserver
```

Open browser to http://127.0.0.1:8000
