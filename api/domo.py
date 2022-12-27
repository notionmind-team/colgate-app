from django.conf import settings
import requests
from base64 import b64encode

def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

def GetAccessToken():
    url = "https://api.domo.com/oauth/token?grant_type=client_credentials&scope=data%20audit%20user%20dashboard"

    payload={}
    headers = {
    'Authorization': basic_auth(settings.DOMO_CLIENT_ID,settings.DOMO_SECRET_ID)
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    return data['token_type'] +" "+data["access_token"]

def GetDomoDashboardList():
    
    url = "https://api.domo.com/v1/pages"
    data = GetAccessToken()

    payload={}
    headers = {
    'Authorization': GetAccessToken()
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()

    return data


