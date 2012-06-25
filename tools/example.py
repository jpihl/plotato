from PlotatoTool import PlotatoTool

#settings:
rest_url    = "http://127.0.0.1:8000/api/v1/"
project_key = ""
test_key    = ""
password    = ""

def main():
    p = PlotatoTool(rest_url)
    print "adding test"
    p.add_test(password, project_key, "Test Test", "This is a test test, created using the rest api.")
    print "adding run"
    p.add_run(password, test_key, ["Hello World!", 42, {"color" : "Bright Yellow", "age" : 32}])
    
    print "getting projects"
    projects = p.get_projects()
    print "total count is {0} projects".format(projects["meta"]["total_count"])
    print "done"

    print "getting project"
    project = p.get_projects("key="+project_key)
    print project["objects"][0]
    print "done"

    print "gettings tests"
    tests = p.get_tests()

    print "total count is {0} tests".format(tests["meta"]["total_count"])
    print "done"

    print "gettings tests from project"
    tests = p.get_tests("project="+project_key)
    print "total count is {0} tests".format(tests["meta"]["total_count"])
    print "done"

    print "gettings atmost 2 tests from project"
    tests = p.get_tests("project="+project_key+"&limit=2")
    print "recieved {0} tests".format(len(tests["objects"]))
    print "done"

    print "getting runs"
    runs = p.get_runs()
    print "total count is {0} runs".format(runs["meta"]["total_count"])
    print "done"

    print "getting runs from test"
    runs = p.get_runs("test="+test_key)
    print "total count is {0} runs".format(runs["meta"]["total_count"])
    print "done"


if __name__ == '__main__':
    main()