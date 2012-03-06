#!/usr/bin/env python
import urllib
import urllib2

def main():

    #settings:
    rest_url = 'http://127.0.0.1:8080/restdata/'
    """
    #Getting data
    response = urllib2.urlopen(rest_url)
    print response.getcode() # Check if the response was ok
    test = eval(response.read()) # Examin the response itself
    print test[0]['project']
    """
    #Inserting data - Dataset
    project_id          = "9313d858-5bc1-11e1-8d2f-001f29a3c04e"
    dataset_name        = "Name of dataset"
    dataset_description = "Description of dataset"
    dataset_unit        = "ms/s*s"

    request_data = urllib.urlencode(
        (
            ('project', project_id),
            ('name', dataset_name),
            ('description', dataset_description),
            ('unit', dataset_unit)
        )
    )
    print request_data
    """
    request = urllib2.Request(
        rest_url,
        data=request_data, 
        headers={'Content-Type':'application/x-www-form-urlencoded'}
    )

    response = urllib2.urlopen(request)
    print response.getcode()

    #Inserting data - DataEntry

    data_entry_revision = 34
    data_entry_value    = 999
    dataset_id          = "989216d8-5bd4-11e1-b6c9-001f29a3c04e"

    request_data = urllib.urlencode(
        (
            ('revision', data_entry_revision),
            ('value', data_entry_value)
        )
    )

    request = urllib2.Request(
        rest_url + dataset_id + "/dataentries/",
        data=request_data,
        headers={'Content-Type':'application/x-www-form-urlencoded'}
    )

    response = urllib2.urlopen(request)
    print response.getcode()
    """

if __name__ == "__main__":
    main()