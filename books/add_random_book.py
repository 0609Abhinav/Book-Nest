import os
import django
import urllib.request
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books.settings')
django.setup()

from senior.models import reg, addbooks, category

# Create or get user
email = 'abhinav@gmail.com'
user, created = reg.objects.get_or_create(
    email=email,
    defaults={
        'name': 'Abhinav',
        'passwd': 'dummy',
        'mobile': '1234567890',
        'city': 'Delhi',
        'is_active': True,
        'is_verified': True
    }
)

# Get or create a category
cat, _ = category.objects.get_or_create(cname='Science Fiction')

# Download dummy image
print("Downloading cover image...")
img_url = 'https://picsum.photos/400/600'
req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
img_content = urllib.request.urlopen(req).read()

# Download dummy pdf
print("Downloading PDF...")
pdf_url = 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf'
req = urllib.request.Request(pdf_url, headers={'User-Agent': 'Mozilla/5.0'})
pdf_content = urllib.request.urlopen(req).read()

# Create book
book = addbooks(
    authorid=user.email,
    bookcategory=cat.cname,
    title='The Great Adventure',
    description='A thrilling journey through the cosmos.',
    useful='For all age groups.',
    charge=0,
    status='approved'
)

# Save files
book.coverpic.save('adventure_cover.jpg', ContentFile(img_content), save=False)
book.bookfile.save('adventure_book.pdf', ContentFile(pdf_content), save=False)
book.save()

print("Book successfully added for abhinav@gmail.com!")
