from django import forms
from django.forms.formsets import BaseFormSet
from .models import *
from .customfields import PhoneNumberField


class ProsceniumTheatreParticipantForm(forms.Form):
    role = forms.ChoiceField(
        choices=ProsceniumParticipant.ROLES,
        initial=ProsceniumParticipant.PERFORMER,
        label="Participant's Role",
        widget=forms.Select(attrs={
            'placeholder': 'Role: Performer / Accompanist',
        }))
    age = forms.IntegerField(
        min_value=1, max_value=25,
        label="Participant's Age",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Age',
        }))
    name = forms.CharField(
        max_length=200,
        label="Participant's Name",
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
        }))
    photo = forms.ImageField(
        validators=[IMAGE_FILE_VALIDATOR],
        max_length=100,
        label="Photo",
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Photo',
        }))


class ProsceniumTheatreRegistrationForm(forms.Form):
    understood = forms.BooleanField()
    referral_code = forms.CharField(
        max_length=50,
        label="Referral Code",
        widget=forms.TextInput(attrs={
            'placeholder': 'Code',
        }), required=False)
    institution = forms.CharField(
        max_length=200,
        label="Name of the Institution",
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
        }))
    language = forms.ChoiceField(
        choices=ProsceniumRegistration.LANGUAGES,
        initial=ProsceniumRegistration.ENGLISH,
        label="Language of the Performance",
        widget=forms.Select(attrs={
            'placeholder': 'Language',
        }))
    prelims_video = forms.FileField(
        validators=[VIDEO_FILE_VALIDATOR],
        label="Video for Prelims",
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Prelims Video',
        }),
        required=False)
    prelims_script = forms.FileField(
        validators=[SCRIPT_FILE_VALIDATOR],
        label="Script for Prelims",
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Prelims Script',
        }),
        required=False)
    contact1 = PhoneNumberField.get_field(
        as_regexField=True,
        max_length=15,
        label="1st Contact No.",
        widget=forms.TextInput(attrs={
            'placeholder': '1st Mobile No.',
        }))
    contact2 = PhoneNumberField.get_field(
        as_regexField=True,
        max_length=15,
        label="2nd Contact No.",
        widget=forms.TextInput(attrs={
            'placeholder': '2nd Mobile No.',
        }),
        required=False)
    email = forms.EmailField(
        label="E-Mail ID",
        widget=forms.TextInput(attrs={
            'placeholder': 'E-Mail ID',
        }))


class ProsceniumTheatreVideoSubmissionForm(forms.Form):
    understood = forms.BooleanField()
    index = forms.IntegerField(
        label="Registration ID",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Registration ID'
        }))
    prelims_video = forms.FileField(
        validators=[VIDEO_FILE_VALIDATOR],
        label="Video for Prelims",
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Prelims Video',
        }))
    prelims_script = forms.FileField(
        validators=[SCRIPT_FILE_VALIDATOR],
        label="Script for Prelims",
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Prelims Script',
        }))


class ProsceniumStreetPlayParticipantForm(forms.Form):
    role = forms.ChoiceField(
        choices=ProsceniumParticipant.ROLES,
        initial=ProsceniumParticipant.PERFORMER,
        label="Participant's Role",
        widget=forms.Select(attrs={
            'placeholder': 'Role: Performer / Accompanist',
        }))
    age = forms.IntegerField(
        min_value=1, max_value=25,
        label="Participant's Age",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Age',
        }))
    name = forms.CharField(
        max_length=200,
        label="Participant's Name",
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
        }))
    photo = forms.ImageField(
        validators=[IMAGE_FILE_VALIDATOR],
        max_length=100,
        label="Photo",
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Photo',
        }))


class ProsceniumStreetPlayRegistrationForm(forms.Form):
    understood = forms.BooleanField()
    referral_code = forms.CharField(
        max_length=50,
        label="Referral Code",
        widget=forms.TextInput(attrs={
            'placeholder': 'Code',
        }), required=False)
    institution = forms.CharField(
        max_length=200,
        label="Name of the Institution",
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
        }))
    language = forms.ChoiceField(
        choices=ProsceniumRegistration.LANGUAGES,
        initial=ProsceniumRegistration.ENGLISH,
        label="Language of the Performance",
        widget=forms.Select(attrs={
            'placeholder': 'Language',
        }))
    contact1 = PhoneNumberField.get_field(
        as_regexField=True,
        max_length=15,
        label="1st Contact No.",
        widget=forms.TextInput(attrs={
            'placeholder': '1st Mobile No.',
        }))
    contact2 = PhoneNumberField.get_field(
        as_regexField=True,
        max_length=15,
        label="2nd Contact No.",
        widget=forms.TextInput(attrs={
            'placeholder': '2nd Mobile No.',
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
        performers, accompanists = 0, 0
        if not forms:
            raise forms.ValidationError("Empty Form", code='empty_form')
        for form in self.forms:
            if form.cleaned_data:
                form_data = tuple(map(str, form.cleaned_data.items()))
                if form_data in data:
                    raise forms.ValidationError(
                        "Possible Duplicate Entry", code='duplicate')
                else:
                    data.add(form_data)
                role = form.cleaned_data['role']
                if role == ProsceniumParticipant.PERFORMER:
                    performers = performers + 1
                elif role == ProsceniumParticipant.ACCOMPANIST:
                    accompanists = accompanists + 1

        if (performers + accompanists) > 10:
            raise forms.ValidationError(
                "You can have a maximum of 7 performers and 3 accompanists", code="over_max_performers_accompanists")
        elif performers == 0:
            raise forms.ValidationError(
                "You must have at least 1 participant", code="no_performers")
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
            'placeholder': 'Mobile No.',
        }))
    name = forms.CharField(max_length=200,
                           label="Participant's Name",
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Name',
                           }))


class BoBRegistrationForm(forms.Form):
    understood = forms.BooleanField()
    referral_code = forms.CharField(
        max_length=50,
        label="Referral Code",
        widget=forms.TextInput(attrs={
            'placeholder': 'Code',
        }), required=False)
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
            'placeholder': 'Genre',
        }),
        required=False)
    facebook_link = forms.URLField(
        label="Link to Facebook Page of the Band",
        widget=forms.URLInput(attrs={
            'placeholder': 'Facebook Page URL',
        }),
        required=False)
    email = forms.EmailField(
        label="E-Mail ID",
        widget=forms.TextInput(attrs={
            'placeholder': 'E-Mail ID',
        }))
    audio_sample_file = forms.FileField(
        validators=[BoBRegistration.AUDIO_FILE_VALIDATOR],
        label="Sample Track File",
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Audio File'
        }),
        required=False)
    audio_sample_link = forms.URLField(
        label="Link to sample track on SoundCloud, ReverbNation or YouTube",
        widget=forms.URLInput(attrs={
            'placeholder': 'Audio URL',
        }),
        required=False)

    def clean(self):
        if any(self.errors):
            return
        super(forms.Form, self).clean()
        audio_sample_link = self.cleaned_data.get('audio_sample_link')
        audio_sample_file = self.cleaned_data.get('audio_sample_file')
        if not (audio_sample_link or audio_sample_file):
            raise forms.ValidationError(
                "You must either upload a sample track or provide a link to one", code='no_sample_audio')


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
                form_data = tuple(map(str, form.cleaned_data.items()))
                if form_data in data:
                    raise forms.ValidationError(
                        "Possible Duplicate Entry", code='duplicate')
                else:
                    data.add(form_data)
                if form.cleaned_data['name'] and form.cleaned_data['contact']:
                    contacts = contacts + 1
        if contacts < 3:
            raise forms.ValidationError(
                "There must be at least 3 participants with a contact no.", code="below_min_contacts")


class LasyaParticipantForm(forms.Form):
    email = forms.EmailField(
        label="E-Mail ID",
        widget=forms.TextInput(attrs={
            'placeholder': "E-Mail ID",
        }))
    contact = PhoneNumberField.get_field(
        as_regexField=True,
        max_length=13,
        label="Contact No.",
        widget=forms.TextInput(attrs={
            'placeholder': 'Mobile No.',
        }))
    name = forms.CharField(max_length=200,
                           label="Participant's Name",
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Name',
                           }))


class LasyaRegistrationForm(forms.Form):
    understood = forms.BooleanField()
    referral_code = forms.CharField(
        max_length=50,
        label="Referral Code",
        widget=forms.TextInput(attrs={
            'placeholder': 'Code',
        }), required=False)
    name = forms.CharField(
        max_length=200,
        label="Your Team Name",
        widget=forms.TextInput(attrs={
            'placeholder': 'Team Name',
        }))
    institution = forms.CharField(
        max_length=200,
        label="Name of Your Institution (if applicable)",
        widget=forms.TextInput(attrs={
            'placeholder': 'Name of Institution',
        }),
        required=False)
    prelims_video = forms.FileField(
        validators=[VIDEO_FILE_VALIDATOR],
        label="Video for Prelims",
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Prelims Video',
        }),
        required=False)
    prelims_video_link = forms.URLField(
        label="Link to Facebook Page of the Band",
        widget=forms.URLInput(attrs={
            'placeholder': 'Facebook Page URL',
        }),
        required=False)
    contact = PhoneNumberField.get_field(
        as_regexField=True,
        max_length=15,
        label="Team's Contact No.",
        widget=forms.TextInput(attrs={
            'placeholder': "Team's Mobile No.",
        }))
    email = forms.EmailField(
        label="Team's E-Mail ID",
        widget=forms.TextInput(attrs={
            'placeholder': "Team's E-Mail ID",
        }))


class LasyaVideoSubmissionForm(forms.Form):
    understood = forms.BooleanField()
    index = forms.IntegerField(
        label="Registration ID",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Registration ID'
        }))
    prelims_video = forms.FileField(
        validators=[VIDEO_FILE_VALIDATOR],
        label="Video for Prelims",
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Prelims Video',
        }))


class BaseLasyaParticipantFormSet(BaseFormSet):

    def clean(self):
        if any(self.errors):
            return
        data = set()
        if not forms:
            raise forms.ValidationError("Empty Form", code='empty_form')
        for form in self.forms:
            if form.cleaned_data:
                form_data = tuple(map(str, form.cleaned_data.items()))
                if form_data in data:
                    raise forms.ValidationError(
                        "Possible Duplicate Entry", code='duplicate')
                else:
                    data.add(form_data)


class SInECParticipantForm(forms.Form):
    institution = forms.CharField(
        max_length=200,
        label="Name of the Institution",
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
        }))
    name = forms.CharField(
        max_length=200,
        label="Participant's Name",
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
        }))
    city = forms.CharField(
        max_length=200,
        label="Your Team's City",
        widget=forms.TextInput(attrs={
            'placeholder': 'City',
        }))
    student_type = forms.ChoiceField(
        choices=SInECParticipant.STUDENT_TYPES,
        initial=SInECParticipant.UG,
        label="Participant's Student Type",
        widget=forms.Select(attrs={
            'placeholder': 'Type of Student: UG/Masters/Ph.D./Post-Doc',
        }))


class SInECRegistrationForm(forms.Form):
    understood = forms.BooleanField()
    referral_code = forms.CharField(
        max_length=50,
        label="Referral Code",
        widget=forms.TextInput(attrs={
            'placeholder': 'Code',
        }), required=False)
    team_name = forms.CharField(
        max_length=200,
        label="Your Team's Name",
        widget=forms.TextInput(attrs={
            'placeholder': 'Team Name',
        }))
    project_name = forms.CharField(
        max_length=200,
        label="The Name of Your Project",
        widget=forms.TextInput(attrs={
            'placeholder': 'Project Name',
        }))
    project_field = forms.CharField(
        max_length=200,
        label="The Field of Your Project",
        widget=forms.TextInput(attrs={
            'placeholder': 'Field of Project',
        }))
    project_abstract = forms.CharField(
        label="Project Abstract (500-1000 words)",
        widget=forms.Textarea(attrs={
            'placeholder': 'Abstract',
        }))
    project_patented = forms.BooleanField(
        label="Has a patent been filed for your project?",
        required=False)
    registered_company = forms.BooleanField(
        label="Are you a registered company?",
        required=False)
    privacy_preference = forms.ChoiceField(
        choices=SInECRegistration.PRIVACY_PREFERENCES,
        initial=SInECRegistration.PRIVATE,
        label="Privacy Preference",
        widget=forms.Select(attrs={
            'placeholder': 'Preference',
        }))
    address = forms.CharField(
        max_length=400,
        label="Address of Your Team",
        widget=forms.TextInput(attrs={
            'placeholder': 'Address',
        }))
    contact = PhoneNumberField.get_field(
        as_regexField=True,
        max_length=15,
        label="Team's Contact No.",
        widget=forms.TextInput(attrs={
            'placeholder': "Team's Mobile No.",
        }))
    email = forms.EmailField(
        label="Team's E-Mail ID",
        widget=forms.TextInput(attrs={
            'placeholder': "Team's E-Mail ID",
        }))
    project_file = forms.FileField(
        label="Project Files (Multiple Files can be Uploaded as a ZIP archive)",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Project File',
        }))

    def clean_project_abstract(self):
        data = self.cleaned_data['project_abstract']
        words = len(data.split())
        if not (500 <= words <= 1000):
            raise forms.ValidationError(f"Project Abstract must be between 500 and 1000 words, was {words} words")
        return data


class BaseSInECParticipantFormSet(BaseFormSet):

    def clean(self):
        if any(self.errors):
            return
        data = set()
        if not forms:
            raise forms.ValidationError("Empty Form", code='empty_form')
        for form in self.forms:
            if form.cleaned_data:
                form_data = tuple(map(str, form.cleaned_data.items()))
                if form_data in data:
                    raise forms.ValidationError(
                        "Possible Duplicate Entry", code='duplicate')
                else:
                    data.add(form_data)


class OpenMicParticipantForm(forms.Form):
    name = forms.CharField(max_length=200,
                           label="Participant's Name",
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Name',
                           }))


class OpenMicRegistrationForm(forms.Form):
    understood = forms.BooleanField()
    referral_code = forms.CharField(
        max_length=50,
        label="Referral Code",
        widget=forms.TextInput(attrs={
            'placeholder': 'Code',
        }), required=False)
    name = forms.CharField(
        max_length=200,
        label="Your Full Name",
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
        }))
    event = forms.CharField(
        max_length=200,
        label="Type of Event",
        widget=forms.TextInput(attrs={
            'placeholder': 'Music/Comedy/Spoken Word/Other',
        }))
    expected_performance_duration_mins = forms.IntegerField(
        label="Expected Performance Duration in Minutes",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Performance Duration (1 - 5 minutes)',
        }),
        min_value=1,
        max_value=5)
    email = forms.EmailField(
        label="E-Mail ID",
        widget=forms.TextInput(attrs={
            'placeholder': 'E-Mail ID',
        }))
    instrument_requirement = forms.CharField(
        max_length=200,
        label="Instruments Required (If Any)",
        widget=forms.TextInput(attrs={
            'placeholder': 'Required Instruments'
        }),
        required=False)
    reason_for_gt_3_members = forms.CharField(
        max_length=400,
        label="Reason for having more than 3 participants",
        widget=forms.TextInput(attrs={
            'placeholder': 'Reason'
        }),
        required=False)

    def __init__(self, *args, **kwargs):
        self.participant_count = kwargs.pop('participant_count', 0)
        super(OpenMicRegistrationForm, self).__init__(*args, **kwargs)

    def clean_reason_for_gt_3_members(self):
        data = self.cleaned_data['reason_for_gt_3_members']
        if 0 < self.participant_count <= 3 and data:
            raise forms.ValidationError("Reason is not required for less than or equal to 3 participants")
        elif self.participant_count > 3 and not data:
            raise forms.ValidationError("Reason is required for more than 3 participants")
        return data



class BaseOpenMicParticipantFormSet(BaseFormSet):

    def clean(self):
        if any(self.errors):
            return
        data = set()
        if not forms:
            raise forms.ValidationError("Empty Form", code='empty_form')
        for form in self.forms:
            if form.cleaned_data:
                form_data = tuple(map(str, form.cleaned_data.items()))
                if form_data in data:
                    raise forms.ValidationError(
                        "Possible Duplicate Entry", code='duplicate')
                else:
                    data.add(form_data)
