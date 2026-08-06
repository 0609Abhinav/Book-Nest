import requests
import time

token = 'c3db0ff4058a11c534ccb0574085a4c291198230'
username = 'abhinavtripathi'
headers = {'Authorization': f'Token {token}'}

print("Fetching consoles...")
resp = requests.get(f'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/', headers=headers)
consoles = resp.json()

if not consoles:
    print("Creating new console...")
    resp = requests.post(f'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/', headers=headers, json={"executable": "bash"})
    console_id = resp.json()['id']
else:
    console_id = consoles[0]['id']
    print(f"Using existing console {console_id}")

commands = """
cd ~/Book-Nest 2>/dev/null || cd ~/Book-Nest- 2>/dev/null
git fetch origin main
git reset --hard origin/main
git pull origin main
cd books
python setup_live.py
"""

print("Sending commands...")
requests.post(f'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{console_id}/send_input/', headers=headers, json={'input': commands})

print("Waiting 15 seconds for execution...")
time.sleep(15)

print("Fetching output...")
out_resp = requests.get(f'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{console_id}/get_latest_output/', headers=headers)
print("OUTPUT:")
print(out_resp.json().get('output', ''))
