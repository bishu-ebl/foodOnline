from django.core.exceptions import ValidationError
import os

def allow_only_image_validator(value):
    ext = os.path.splitext(value.name)[1] # where 1 refer to the extention of a file
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        # here we use str to covert valid_extension into string, because valid_extension is dictionary type
        # but we are concanating with string type text, which is not supported
        raise ValidationError('Unsupported file extensions. Allowed extension: ' + str(valid_extensions))