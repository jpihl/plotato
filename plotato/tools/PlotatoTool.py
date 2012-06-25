import urllib
import urllib2
import json

class PlotatoTool:
    def __init__(self, _url):
        """Initiates the PlotatoTool.

        Keyword arguments:
        _url -- The url to the plotato rest URL, e.g. "http://127.0.0.1:8000/api/v1/"

        """
        self.url = _url

    def get_projects(self, args = ""):
        """Retrieves projects in plotato.

        Keyword arguments:
        args -- The argumentes seperated by "&" for filtering the retrieval,
                e.g. use "slug__startswith=test&created_lte=2012-06-22T22:35:44.272185+00:00"
                to get the projects which starts with "test", and was created before the timestamp

        """
        response = urllib2.urlopen(self.url+"project/?format=json&" + args) 
        return json.loads(response.read())

    def get_tests(self, args = ""):
        """Retrieves tests in plotato.

        Keyword arguments:
        args -- The argumentes seperated by "&" for filtering the retrieval,
                e.g. use "slug__startswith=test&created_lte=2012-06-22T22:35:44.272185+00:00"
                to get the tests which starts with "test", and was created before the timestamp
        
        """
        response = urllib2.urlopen(self.url+"test/?format=json&" + args)
        return json.loads(response.read())

    def get_runs(self, args = ""):
        """Retrieves runs in plotato.

        Keyword arguments:
        args -- The argumentes seperated by "&" for filtering the retrieval
        
        """
        response = urllib2.urlopen(self.url+"run/?format=json&" + args)
        return json.loads(response.read())

    def add_test(self, password, project_key, test_name, test_description):
        """Adds a tests to a project.

        Keyword arguments:
        password         -- The admin password.
        project_key      -- The key of the project which is to have the new test
        test_name        -- the name of the new test
        test_description -- the description of the new test

        """
        request_data = json.dumps(
            {
                'project': "/api/v1/project/" + project_key + "/",
                'name': test_name,
                'description': test_description,
            }
        )
        self.__add_request_data(password, "test", request_data)

    def add_run(self, password, test_key, data):
        """Adds a run to a test.

        Keyword arguments:
        password -- The admin password.
        test_key -- The key of the test which is to have the new run
        data     -- the data of the new run
        
        """
        request_data = json.dumps(
            {
                'test': "/api/v1/test/" + test_key + "/",
                'data': data,
            }
        )
        self.__add_request_data(password, "run", request_data)

    def __add_request_data(self, password, kind, request_data):
        request = urllib2.Request(
            self.url + kind + "/",
            data=request_data,
            headers={'Content-Type':'application/json',
                     'X-PLOTATO-PASSWORD': password}
        )

        try:
            response = urllib2.urlopen(request)
            print response.msg
        except urllib2.HTTPError, error:
            print 'ERROR {0}'.format(error.code)
            print error.msg