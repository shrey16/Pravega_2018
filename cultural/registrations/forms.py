from django import forms
from django.forms.formsets import BaseFormSet
from .models import *
from .customfields import PhoneNumberField


class ProsceniumTheatreParticipantForm(forms.Form):
    role = forms.ChoiceField(
        choices=ProsceniumTheatreParticipant.ROLES,
        initial=ProsceniumTheatreParticipant.PARTICIPANT,
        label="Participant's Role",
        required=True,
        widget=forms.Select(attrs={
            'placeholder': 'Role: Participant / Accompanist',
        }))
    age = forms.IntegerField(
        min_value=1, max_value=25,
        label="Participant's Age",
        required=True,
        widget=forms.NumberInput(attrs={
                                 'placeholder': 'Age',
                                 }))
    name = forms.CharField(
        max_length=200,
        label="Participant's Name",
        required=True,
        widget=forms.TextInput(attrs={
                               'placeholder': 'Name of Participant',
                               }))


class ProsceniumTheatreRegistrationForm(forms.Form):
    institution = forms.CharField(
        max_length=200,
        label="Name of the Institution",
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
        }))
    language = forms.ChoiceField(
        choices=ProsceniumTheatreRegistration.LANGUAGES,
        initial=ProsceniumTheatreRegistration.ENGLISH,
        label="Language of the Performance",
        widget=forms.Select(attrs={
            'placeholder': 'Role: Participant / Accompanist',
        }))
    prelims_video = forms.FileField(
        validators=[ProsceniumTheatreRegistration.VIDEO_FILE_VALIDATOR],
        label="Video for Prelims",
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Prelims Video',
        }))
    prelims_script = forms.FileField(
        validators=[ProsceniumTheatreRegistration.SCRIPT_FILE_VALIDATOR],
        label="Script for Prelims",
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Prelims Script',
        }))
    contact1 = PhoneNumberField.get_field(
        as_regexField=True,
        max_length=15,
        label="1st Contact No.",
        widget=forms.TextInput(attrs={
            'placeholder': '1st Contact No.',
        }))
    contact2 = PhoneNumberField.get_field(
        as_regexField=True,
        max_length=15,
        label="2nd Contact No.",
        widget=forms.TextInput(attrs={
            'placeholder': '2nd Contact No.',
        }),
        required=False)
    email = forms.EmailField(
        label="E-Mail ID",
        widget=forms.TextInput(attrs={
            'placeholder': 'E-Mail ID',
        }))


class ProsceniumStreetPlayParticipantForm(forms.Form):
    role = forms.ChoiceField(choices=ProsceniumStreetPlayParticipant.ROLES,
                             initial=ProsceniumStreetPlayParticipant.PARTICIPANT,
                             label="Participant's Role",
                             widget=forms.Select(attrs={
                                 'placeholder': 'Role: Participant / Accompanist',
                             }))
    age = forms.IntegerField(min_value=1, max_value=25,
                             label="Participant's Age",
                             widget=forms.NumberInput(attrs={
                                 'placeholder': 'Age',
                             }))
    name = forms.CharField(max_length=200,
                           label="Participant's Name",
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Name of Participant',
                           }))
    photo = forms.ImageField(
        validators=[ProsceniumStreetPlayParticipant.IMAGE_FILE_VALIDATOR],
        max_length=100,
        label="Photo",
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Photo',
        }))


class ProsceniumStreetPlayRegistrationForm(forms.Form):
    institution = forms.CharField(
        max_length=200,
        label="Name of the Institution",
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
        }))
    language = forms.ChoiceField(
        choices=ProsceniumStreetPlayRegistration.LANGUAGES,
        initial=ProsceniumStreetPlayRegistration.ENGLISH,
        label="Language of the Performance",
        widget=forms.Select(attrs={
            'placeholder': 'Role: Participant / Accompanist',
        }))
    contact1 = PhoneNumberField.get_field(
        as_regexField=True,
        max_length=15,
        label="1st Contact No.",
        widget=forms.TextInput(attrs={
            'placeholder': '1st Contact No.',
        }))
    contact2 = PhoneNumberField.get_field(
        as_regexField=True,
        max_length=15,
        label="2nd Contact No.",
        widget=forms.TextInput(attrs={
            'placeholder': '2nd Contact No.',
        }),
        required=False)
    email = forms.EmailField(
        label="E-Mail ID",
        widget=forms.TextInput(attrs={
            'placeholder': 'E-Mail ID',
        }))


class BaseProsceniumParticipantFormSet(BaseFormSet):
    MAX_PARTCIPANTS, MAX_ACCOMPANISTS = 10, 3

    def clean(self):
        if any(self.errors):
            return
        data = set()
        participants, accompanists = 0, 0
        if not forms:
            raise forms.ValidationError("Empty Form", code='empty_form')
        for form in self.forms:
            if form.cleaned_data:
                form_data = tuple(form.cleaned_data.items())
                if form_data in data:
                    raise forms.ValidationError("Duplicate Entry", code='duplicate')
                else:
                    data.add(form_data)
                role = form.cleaned_data['role']
                if role == ProsceniumTheatreParticipant.PARTICIPANT or role == ProsceniumStreetPlayParticipant.PARTICIPANT:
                    participants = participants + 1
                elif role == ProsceniumTheatreParticipant.ACCOMPANIST or role == ProsceniumStreetPlayParticipant.ACCOMPANIST:
                    accompanists = accompanists + 1

                if not form.cleaned_data['name']:
                    raise forms.ValidationError(
                        "Please Enter a Name", code="no_name")
                if not form.cleaned_data['age']:
                    raise forms.ValidationError(
                        "Please Enter an Age", code="no_age")

        if participants > 10 and accompanists > 3:
            raise forms.ValidationError(
                "You can have a maximum of 10 participants and 3 accompanists", code="over_max_participants_accompanists")
        elif participants == 0:
            raise forms.ValidationError(
                "You must have at least 1 participant", code="no_participants")
        elif participants > 10:
            raise forms.ValidationError(
                "You can have a maximum of 10 participants", code="over_max_participants")
        elif accompanists > 3:
            raise forms.ValidationError(
                "You can have a maximum of 3 accompanists", code="over_max_accompanists")


class BoBParticipantForm(forms.Form):
    instrument = forms.CharField(max_length=200,
                                 label="Participant's Instrument",
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Instrument',
                                 }))
    contact = PhoneNumberField.get_field(
        as_regexField=True,
        max_length=15,
        label="Contact No.",
        widget=forms.TextInput(attrs={
            'placeholder': 'Contact No.',
        }))
    name = forms.CharField(max_length=200,
                           label="Participant's Name",
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Name of Participant',
                           }))


class BoBRegistrationForm(forms.Form):
    band_name = forms.CharField(
        max_length=200,
        label="Name of the Band",
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
        }))
    city = forms.CharField(
        max_length=200,
        label="Your Band's City",
        widget=forms.TextInput(attrs={
            'placeholder': 'City',
        }))
    prelims_venue = forms.ChoiceField(
        choices=BoBRegistration.PRELIMS_VENUES,
        initial=BoBRegistration.BANGALORE,
        label="Choice of Prelims Venue",
        widget=forms.Select(attrs={
            'placeholder': 'City',
        }))
    genre = forms.CharField(
        max_length=100,
        label="Genre of Music",
        widget=forms.TextInput(attrs={
            'placeholder': 'Genre.',
        }))
    facebook_link = forms.URLField(
        label="Link to Facebook Page of the Band",
        widget=forms.URLInput(attrs={
            'placeholder': 'Facebook Page URL',
        }))
    email = forms.EmailField(
        label="E-Mail ID",
        widget=forms.TextInput(attrs={
            'placeholder': 'E-Mail ID',
        }))
    audio_sample = forms.FileField(
        validators=[BoBRegistration.AUDIO_FILE_VALIDATOR],
        label="A Sample Audio Track of Your Band",
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Audio File'
        }))


class BaseBoBParticipantFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        contacts = 0
        data = set()
        if not forms:
            raise forms.ValidationError("Empty Form", code='empty_form')
        for form in self.forms:
            if form.cleaned_data:
                form_data = tuple(form.cleaned_data.items())
                if form_data in data:
                    raise forms.ValidationError("Duplicate Entry", code='duplicate')
                else:
                    data.add(form_data)
                contact = form.cleaned_data['contact']
                if form.cleaned_data['name'] and contact:
                    contacts = contacts + 1
        if contacts < 3:
            raise forms.ValidationError(
                "There must be at least 3 participants with a contact no.", code="below_min_contacts")
