from django.db import models
from django import forms
from django.core.validators import RegexValidator


class PhoneNumberField():
    phone_regex = r'^\+91\d{10}$|^0\d{10}$|^\d{10}$'
    message = "Phone number must be entered in the format: '+91----------'. 12 digits allowed."

    def get_field(as_regexField=False, *args, **kwargs):
        if as_regexField:
            return forms.RegexField(regex=PhoneNumberField.phone_regex, help_text=PhoneNumberField.message, *args, **kwargs)
        else:
            return models.CharField(validators=[RegexValidator(regex=PhoneNumberField.phone_regex,
                                                               message=PhoneNumberField.message)], max_length=15, blank=True)
