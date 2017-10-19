from django.db import models
from django import forms
from django.core.validators import RegexValidator


class SeparatedValuesField(models.TextField):

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def from_db_value(self, value):
        return self.to_python(value)

    def get_db_prep_value(self, value):
        if not value:
            return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([s for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class PhoneNumberField():
    phone_regex = r'^\+?1?\d{9,15}$|^$'
    message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."

    def get_field(as_regexField=False, *args, **kwargs):
        if as_regexField:
            return forms.RegexField(regex=PhoneNumberField.phone_regex, help_text=PhoneNumberField.message, *args, **kwargs)
        else:
            return models.CharField(validators=[RegexValidator(regex=PhoneNumberField.phone_regex,
                                                               message=PhoneNumberField.message)], max_length=15, blank=True)


class IntegerRangeField(models.IntegerField):

    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
