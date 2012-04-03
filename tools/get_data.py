#!/usr/bin/env python
import urllib
import urllib2
import json

#settings:
plotato_rest_url = 'http://127.0.0.1:8080/api/v1/'

def main():
    get_projects()
    get_tests()
    get_runs()
    get_users()

def get_projects():
    print "Getting Projects..."
    response = urllib2.urlopen(plotato_rest_url+"project/?format=json") #Send request and recieve respons
    projects = json.loads(response.read())
    for project in projects["objects"]:
        print project["name"] + "\t-\t" + project["key"]

def get_tests():
    print "Getting Tests..."
    response = urllib2.urlopen(plotato_rest_url+"test/?format=json") #Send request and recieve respons
    tests = json.loads(response.read())
    for test in tests["objects"]:
        print test["name"] + "\t-\t" + test["key"]

def get_runs():
    print "Getting Runs..."
    response = urllib2.urlopen(plotato_rest_url+"run/?format=json") #Send request and recieve respons
    runs = json.loads(response.read())
    for run in runs["objects"]:
        print run["key"]

def get_users():
    print "Getting Users..."
    response = urllib2.urlopen(plotato_rest_url+"user/?format=json") #Send request and recieve respons
    users = json.loads(response.read())
    for user in users["objects"]:
        print user["username"]

if __name__ == "__main__":
    main()