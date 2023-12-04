from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    if value > int(datetime.now().year):
        raise ValidationError('Год не может быть в будущем')
