import requests
import urllib3

urllib3.disable_warnings()

BASEURL = 'https://131.104.49.102/api'

def test_base_url():
    r = requests.get(BASEURL, verify=False)
    if not r.ok:
        return False

    if r.text == 'Hello world!':
        return True
    return False

def test_get_course():
    r = requests.get(BASEURL + '/course/cis3110', verify=False)
    if not r.ok:
        return False

    # what the request should get if the api is working correctly
    expected_response = {
        "code": "CIS*3110",
        "coreqs": "",
        "de": False,
        "department": "School of Computer Science",
        "description": "This course covers operating systems in theory and practice by focusing on the components in a system: scheduling, resource allocation, process management, multi-programming, multi-tasking, I/O control, file systems, and mechanisms for client-server computing using examples from contemporary operating systems.",
        "location": "Guelph",
        "name": "Operating Systems I",
        "prereqs": {
            "eq_prereqs": [
                ["CIS*2030", "ENGG*2410"]
            ],
            "reg_prereqs": ["CIS*2520"]
        },
        "restrictions": "",
        "terms": ["W"],
        "weight":0.5
    }

    if r.json() == expected_response:
        return True
    return False

def test_get_courses():
    r = requests.get(BASEURL + '/courses?name=intro&weight=0.5&terms=F', verify=False)
    if not r.ok:
        return False

    if len(r.json()) == 57:
        return True
    return False
