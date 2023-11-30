from django.core.exceptions import ValidationError


def validate_passport(
    passport,
):
    if len(passport) != 8:
        raise ValidationError("Passport should consist 8 characters")
    elif not passport[:2].isupper() or not passport[:2].isalpha():
        raise ValidationError("First 2 characters should be uppercase letters")
    elif not passport[2:].isdigit():
        raise ValidationError("Last 6 characters should be digits")
    return passport
