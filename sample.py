import urllib.parse
import requests

api_key="799f29c7-42e2-4a7e-9c14-9c0f3b2c936f"
secret_key="j99vbuqsh8"
rurl = urllib.parse.quote('https://127.0.0.1:5000/',safe="")
uri = f"https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={api_key}&redirect_uri={rurl}"
print(uri)
code="cZnYvO"

url = 'https://api.upstox.com/v2/login/authorization/token'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
    'code': code,
    'client_id': api_key,
    'client_secret': secret_key,
    'redirect_uri': 'https://127.0.0.1:5000/',
    'grant_type': 'authorization_code',
}

response = requests.post(url, headers=headers, data=data)

print(response.status_code)
print(response.json()['access_token'])