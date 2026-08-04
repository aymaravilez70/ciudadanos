import requests

tokens = [
    "i2ms5b4IT4mISObdHtzxzFQ83SS1S9o4WryDWD8cShE",
]

for token in tokens:
    url = f"https://consultas.ec/credits?token={token}"
    try:
        r = requests.get(url, timeout=10)
        print(f"Token: {token}")
        print(f"Status Code: {r.status_code}")
        print(f"Response: {r.text}")
        print("-" * 50)
    except Exception as e:
        print(f"Error checking token {token}: {e}")
