from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from rest_framework.validators import UniqueTogetherValidator, qs_exists


def validate_forbidden_usernames(value):
    """Checks that username is not in forbidden values."""

    if value in settings.FORBIDDEN_USERNAMES:
        raise ValidationError(f'"{value}" username is forbidden.')


class ValidateUniqueFields:
    """Checks that fields is unique.
    Do not raise ValidationError, if all fields
    belongs to single instance
    """

    message = gettext_lazy('The fields {field_names} must make a unique set.')

    def __init__(self, queryset, fields):
        self.queryset = queryset
        self.fields = fields

    def __call__(self, attrs):
        queryset = self.queryset
        for field, value in attrs.items():
            obj = queryset.filter(**{field: value}).first()
            if obj:
                attrs.pop(field)
                for obj_field, val in attrs.items():
                    if getattr(obj, obj_field) != val:
                        raise ValidationError(
                            f'"{value}" usgdgsername is forbidden.'
                        )
                return
