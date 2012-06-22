#!/usr/bin/env python
import urllib
import urllib2
import json
try:
  import cPickle as pickle
except ImportError:
  import pickle


#settings:
rest_url = 'http://127.0.0.1:8000/api/v1/'


def main():
    #add_test()
    add_run()

def add_test():
    print "Adding Test..."
    #settings:
    project_key      = "562042d2-9dd5-11e1-84e4-001f29a3c04e"
    project          = "/api/v1/project/" + project_key + "/"
    test_name        = "test name"
    test_description = "test description"

    request_data = json.dumps(
        {
            'project': project,
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
        print response.msg
    except urllib2.HTTPError, error:
        print 'ERROR {0}'.format(error.code)
        print error.msg

def add_run():
    print "Adding Run..."
    #settings:
    test_key      = "6ee0617c-a83d-11e1-82ca-001f29a3c04e"
    test          = "/api/v1/test/" + test_key + "/"
    
    data          = [{"revison": 42, "value": "Very Pink!", "List of Death": [1,2,3,4,5]}]
    
    request_data = json.dumps(
        {
            'test': test,
            'data': data,
            
        }
    )
    print request_data

    request = urllib2.Request(
        rest_url + "run/",
        data=request_data,
        headers={'Content-Type':'application/json',
                 'X-PLOTATO-APIKEY': "5d90b5147be6adb3ba6c799fa7466d424f44361a",
                 'X-PLOTATO-USERNAME': "wahwah"}
    )

    try:
        response = urllib2.urlopen(request)
        print response.msg
    except urllib2.HTTPError, error:
        print 'ERROR {0}'.format(error.code)
        print error.msg

if __name__ == '__main__':
    main()