import requests

token = 'c3db0ff4058a11c534ccb0574085a4c291198230'
username = 'abhinavtripathi'  # API username (lowercase)
pa_home = 'Abhinavtripathi'   # Actual home dir (capital A!)
domain = f'{username}.pythonanywhere.com'
headers = {'Authorization': f'Token {token}'}

files_to_upload = [
    'books/templates/senior/index.html',
    'books/templates/senior/book_detail.html',
    'books/templates/senior/latestbooks.html',
    'books/templates/base.html',
    'books/static/css/global.css',
    'books/books/settings.py',
    'books/senior/views.py',
    'books/senior/utils.py',
    'books/.env',
]

print("=== Uploading files ===")
for filepath in files_to_upload:
    remote_path = f'/home/{pa_home}/Book-Nest/{filepath}'
    with open(filepath, 'rb') as f:
        content = f.read()
    
    r = requests.post(
        f'https://www.pythonanywhere.com/api/v0/user/{username}/files/path{remote_path}',
        headers=headers,
        files={'content': (filepath.split('/')[-1], content)}
    )
    print(f"  {filepath}: {r.status_code} - {r.text[:150]}")

# Reload
print("\n=== Reloading web app ===")
r = requests.post(
    f'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain}/reload/',
    headers=headers
)
print(f"Reload: {r.status_code}")

# Verify
print("\n=== Verifying ===")
r = requests.get(
    f'https://www.pythonanywhere.com/api/v0/user/{username}/files/path/home/{pa_home}/Book-Nest/books/templates/senior/index.html',
    headers=headers
)
if r.status_code == 200:
    has_hero_section = 'hero-section' in r.text
    has_swiper = 'heroSwiper' in r.text
    print(f"  Contains 'hero-section' (NEW): {has_hero_section}")
    print(f"  Contains 'heroSwiper' (OLD): {has_swiper}")
    if has_hero_section and not has_swiper:
        print("  SUCCESS!")
    else:
        print("  FAILED - old code still present")
else:
    print(f"  Read failed: {r.status_code}")
