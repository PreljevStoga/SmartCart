import requests
import json


# url = 'http://localhost:8000/potvrdi_lozinku'
# x = requests.post(url, data={'token': 202406, 'email': 'ante@fer.hr'}, timeout=2.5)

# url = 'http://localhost:8000/android/login'
# x = requests.post(url, json={'email': 'trgovac@fer.hr', 'password': 'pwd'}, timeout=2.5)

# url = 'http://localhost:8000/android/logout'
# x = requests.post(url, json={'sessionId': 'neki session id'}, timeout=2.5)
#################
"""
url = 'http://localhost:8000/android/login'
x = requests.post(url, json={'email': 'trgovac@fer.hr', 'password': 'pwd'}, timeout=2.5)

print(x.json())
sessionId = x.json()['session_id']

url = 'http://localhost:8000/android/edit_profile'
x = requests.post(url, json={'session_id': sessionId, 'password': 'abc'})

url = 'http://localhost:8000/android/artiklitrgovina'
x = requests.post(url, json={'sif_trgovina': '1'}, timeout=2.5)

url = 'http://localhost:8000/android/artikltrgovina'
x = requests.post(url, json={'sif_trgovina': '1', 'barkod': '3850104008597'}, timeout=2.5)

url = 'http://localhost:8000/android/opisi'
x = requests.post(url, json={'sif_trgovina': '1', 'barkod': '3850104008597'}, timeout=2.5)
"""

url = 'http://localhost:8000/android/artiklitrgovina'
x = requests.post(url, json={'sif_trgovina': '1'}, timeout=2.5)

try:
    a = x.json()
    for z in a:
        print(z)
    print("dan je json")
except:
    print(x.text)
    print("dan je x")