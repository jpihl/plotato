#!/usr/bin/env python
import urllib
import urllib2
import json

#settings:
rest_url = 'http://127.0.0.1:8080/api/v1/'

def main():
    #add_project()
    #add_test()
    add_run()

def add_project():
    print "Adding Project..."
    #settings:
    project_name = "project name"
    project_description = "project description"

    request_data = json.dumps({'name': project_name, 'description': project_description,})

    request = urllib2.Request(
        rest_url + "project/",
        data=request_data, 
        headers={'Content-Type':'application/json'}
    )
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, error:
        print error.read()

def add_test():
    print "Adding Test..."
    #settings:
    project_key      = "/api/v1/project/b3f1a4e0-7d06-11e1-89a3-001f29a3c04e/"
    test_name        = "test name"
    test_description = "test description"

    request_data = json.dumps(
        {
            'project': project_key,
            'name': test_name,
            'description': test_description,
        }
    )
    request = urllib2.Request(
        rest_url + "test/",
        data=request_data, 
        headers={'Content-Type':'application/json'}
    )
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, error:
        print error.read()

def add_run():
    print "Adding Run..."
    #settings:
    test_key      = "8ded8058-7d0f-11e1-a41c-001f29a3c04e"
    test          = "/api/v1/test/" + test_key + "/"
    data          = {"revison": 42, "value": "Very Pink!", "List of Death": [1,2,3,4,5]}


    request_data = json.dumps(
        {
            'test': test,
            'data': data
        }
    )
    request = urllib2.Request(
        rest_url + "run/",
        data=request_data, 
        headers={'Content-Type':'application/json'}
    )
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, error:
        print error.read()

if __name__ == '__main__':
    main()