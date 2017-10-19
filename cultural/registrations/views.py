from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError, transaction
from django.forms.formsets import formset_factory
from .forms import *
from .models import *


def index(request):
    return HttpResponse("Move on folks, nothing to see here!")


def proscenium(request):
    ProsceniumParticipantFormSet = formset_factory(
        ProsceniumParticipantForm, formset=BaseProsceniumParticipantFormSet)
    registration = ProsceniumRegistration()

    registration_form = ProsceniumRegistrationForm()
    participant_formset = ProsceniumParticipantFormSet()

    if request.method == 'POST':
        registration_form = ProsceniumRegistrationForm(request.POST)
        participant_formset = ProsceniumParticipantFormSet(request.POST)

        context = {
            'registration_form': registration_form,
            'participant_formset': participant_formset
        }

        if registration_form.is_valid() and participant_formset.is_valid():
            registration.institution = registration_form.cleaned_data.get(
                'institution')
            registration.contact1 = registration_form.cleaned_data.get(
                'contact1')
            registration.contact2 = registration_form.cleaned_data.get(
                'contact2')
            registration.email = registration_form.cleaned_data.get('email')
            registration.save()

            participants = []
            for participant_form in participant_formset:
                name = participant_form.cleaned_data.get('name')
                age = participant_form.cleaned_data.get('age')
                role = participant_form.cleaned_data.get('role')

                if name and age and role:
                    participants.append(ProsceniumParticipant(
                        registration_entry=registration, name=name, age=age, role=role))

            try:
                with transaction.atomic():
                    ProsceniumParticipant.objects.filter(
                        registration_entry=registration).delete()
                    ProsceniumParticipant.objects.bulk_create(participants)
                return redirect("http://pravega.org/proscenium.html")
            except IntegrityError:
                return render(request, "proscenium.html", context.update({'error_message': "Error saving participant data. Please retry."}))
        else:
            return render(request, "proscenium.html", context.update({'error_message': "Check your input, it might be incorrect."}))
    else:
        context = {
            'registration_form': registration_form,
            'participant_formset': participant_formset
        }
        return render(request, "proscenium.html", context)
