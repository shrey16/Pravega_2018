from django import forms
from django.forms.formsets import BaseFormSet
from .models import ProsceniumParticipant
from .customfields import PhoneNumberField


class ProsceniumParticipantForm(forms.Form):
    role = forms.ChoiceField(choices=ProsceniumParticipant.ROLES,
                             initial=ProsceniumParticipant.PARTICIPANT,
                             label="Participant's Role",
                             widget=forms.Select(attrs={
                                 'placeholder': 'Role: Participant / Accompanist',
                             }),
                             required=True)
    age = forms.IntegerField(min_value=1, max_value=25,
                             label="Participant's Age",
                             widget=forms.NumberInput(attrs={
                                 'placeholder': 'Age',
                             }),
                             required=True)
    name = forms.CharField(max_length=200,
                           label="Participant's Name",
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Name of Participant',
                           }),
                           required=True)


class ProsceniumRegistrationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ProsceniumRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['institution'] = forms.CharField(
            max_length=200,
            label="Name of the Institution",
            widget=forms.TextInput(attrs={
                'placeholder': 'Name of the Institution',
            }))
        self.fields['contact1'] = PhoneNumberField.get_field(
            as_regexField=True,
            max_length=15,
            label="1st Contact No.",
            widget=forms.TextInput(attrs={
                'placeholder': '1st Contact No.',
            }))
        self.fields['contact2'] = PhoneNumberField.get_field(
            as_regexField=True,
            max_length=15,
            label="2nd Contact No.",
            widget=forms.TextInput(attrs={
                'placeholder': '2nd Contact No.',
            }),
            required=False)
        self.fields['email'] = forms.EmailField(
            label="E-Mail ID",
            widget=forms.TextInput(attrs={
                'placeholder': 'E-Mail ID',
            }))


class BaseProsceniumParticipantFormSet(BaseFormSet):
    MAX_PARTCIPANTS, MAX_ACCOMPANISTS = 10, 3

    def clean(self):
        if any(self.errors):
            return
        participants, accompanists = 0, 0
        for form in self.forms:
            if form.cleaned_data:
                role = form.cleaned_data['role']
                if role == ProsceniumParticipant.PARTICIPANT:
                    participants = participants + 1
                elif role == ProsceniumParticipant.ACCOMPANIST:
                    accompanists = accompanists + 1
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
