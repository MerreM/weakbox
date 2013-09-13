import requests
import json

def getToken():
    response = requests.post("http://127.0.0.1:8000/api/register/")
    token = json.loads(response.content)
    return token

def testClient():
    token = getToken()
    response = requests.post("http://127.0.0.1:8000/api/store/key//",data=token)
    print response
    response = requests.post("http://127.0.0.1:8000/api/store/storeMe/Value/",data=token)
    print response
    response = requests.post("http://127.0.0.1:8000/api/retrieve/key/",data=token)
    print response
    response = requests.post("http://127.0.0.1:8000/api/retrieve/",data=token)
    print response
    response = requests.post("http://127.0.0.1:8000/api/store/tooolongkeynamevaluestorethrowanerror//",data=token)
    ## This error could be more informative.
    print response


if __name__ == "__main__":
    testClient()