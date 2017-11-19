from django.db import models
from django import forms
from django.core.validators import RegexValidator


class PhoneNumberField():
    phone_regex = r'^\+91\d{10}$|^0\d{10}$|^\d{10}$'
    message = "Please enter a valid 10 digit phone number, prefixed by either 0, +91, or nothing"
    error_messages = {
        'required': 'This field is required',
        'invalid': message
    }

    def get_field(as_regexField=False, *args, **kwargs):
        if as_regexField:
            return forms.RegexField(regex=PhoneNumberField.phone_regex, help_text=PhoneNumberField.message, error_messages=PhoneNumberField.error_messages, *args, **kwargs)
        else:
            return models.CharField(validators=[RegexValidator(regex=PhoneNumberField.phone_regex,
                                                               message=PhoneNumberField.message)], max_length=15, blank=True)
