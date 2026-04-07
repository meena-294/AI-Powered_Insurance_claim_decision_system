import requests

res = requests.post(
    "http://127.0.0.1:7861/api/predict/state",
    json={"data": []}
)

print(res.json())