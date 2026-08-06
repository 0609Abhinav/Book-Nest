import requests

token = 'c3db0ff4058a11c534ccb0574085a4c291198230'
username = 'abhinavtripathi'
domain = 'abhinavtripathi.pythonanywhere.com'
headers = {'Authorization': f'Token {token}'}

mappings = [
    ('/static/signup/', '/home/Abhinavtripathi/Book-Nest/books/static/signup'),
    ('/static/category/', '/home/Abhinavtripathi/Book-Nest/books/static/category'),
    ('/static/newrelesed/', '/home/Abhinavtripathi/Book-Nest/books/static/newrelesed'),
    ('/static/city/', '/home/Abhinavtripathi/Book-Nest/books/static/city'),
    ('/static/addbooks/', '/home/Abhinavtripathi/Book-Nest/books/static/addbooks'),
    ('/static/bookfiles/', '/home/Abhinavtripathi/Book-Nest/books/static/bookfiles')
]

for url, path in mappings:
    resp = requests.post(f'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain}/static_files/', headers=headers, json={'url': url, 'path': path})
    print(f"Added {url}: {resp.status_code}")

resp = requests.post(f'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain}/reload/', headers=headers)
print("Reloaded app:", resp.status_code)
