from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from PIL import Image

def validate_image_size(image):
    img = Image.open(image)
    if img.width > 600 or img.height > 600:
        raise ValidationError(
            _('Ошибка (неверное разрешение файла)'),
            params={'width': img.width, 'height': img.height},
        )
