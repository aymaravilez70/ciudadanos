import requests

try:
    r = requests.get("https://consultas.ec/credits?token=cYd9cAoaL24I5G2i391avPBuIuldBw1uU3myE8XwYAY", timeout=10)
    print(f"Credits Response: {r.status_code} - {r.text}", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
