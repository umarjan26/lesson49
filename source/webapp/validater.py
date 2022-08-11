from django.core.exceptions import ValidationError


def validate_summary(value):
    error_element = ['!']
    for i in error_element:
        if i in value:
            raise ValidationError(f"Название не должно содержать символ '{i}'")
        return value
