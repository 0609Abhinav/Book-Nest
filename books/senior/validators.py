from django.core.exceptions import ValidationError
import os

def validate_image_file(file):
    max_size = 2 * 1024 * 1024 # 2MB
    valid_extensions = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(file.name)[1].lower()
    
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed: jpg, jpeg, png.')
    if file.size > max_size:
        raise ValidationError('Image size cannot exceed 2MB.')

def validate_pdf_file(file):
    max_size = 10 * 1024 * 1024 # 10MB
    ext = os.path.splitext(file.name)[1].lower()
    
    if ext != '.pdf':
        raise ValidationError('Only PDF files are allowed for books.')
    if file.size > max_size:
        raise ValidationError('PDF size cannot exceed 10MB.')
