#!/usr/bin/env python
import requests

API_ROOT = "http://127.0.0.1:8001/api/{}"


def get_token():
    response = requests.post(API_ROOT.format("register/"))
    return response.json()


def test_client():
    token = get_token()
    response = requests.post(API_ROOT.format("store/key//"), data=token)
    print(response)

    response = requests.post(API_ROOT.format(
        "store/storeMe/Value/"), data=token)
    print(response)

    response = requests.post(
        API_ROOT.format("retrieve/key/"), data=token)
    print(response)

    response = requests.post(API_ROOT.format("retrieve/"), data=token)
    print(response)

    response = requests.post(
        API_ROOT.format(
            "store/tooolongkeynamevaluestorethrowanerror//"), data=token)
    print(response)


if __name__ == "__main__":
    test_client()
