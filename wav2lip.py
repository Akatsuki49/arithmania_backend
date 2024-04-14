import requests

url = "https://api.d-id.com/talks"

payload = {
    "script": {
        "type": "text",
        "subtitles": "false",
        "provider": {
            "type": "microsoft",
            "voice_id": "en-US-JennyNeural"
        },
        "input": "Hello"
    },
    "config": {
        "fluent": "false",
        "pad_audio": "0.0"
    },
    "source_url": "x"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Basic YzJoMVltaGhiV1p2ZURFd1FHZHRZV2xzTG1OdmJROkRrSWpISklHbU12Zmp0WkhHek1vYQ=="
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)