from django.conf import settings
from django.core.exceptions import ValidationError


def validate_forbidden_usernames(value):
    """Checks that username is not in forbidden values."""

    if value in settings.FORBIDDEN_USERNAMES:
        raise ValidationError(f'"{value}" username is forbidden.')
