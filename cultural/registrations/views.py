from django.shortcuts import render, redirect
from django.db import IntegrityError, transaction
from django.forms.formsets import formset_factory
from .forms import *
from .models import *


def index(request):
    return render(request, "index.html", {})


def proscenium(request):
    return render(request, "proscenium.html", {})


def proscenium_theatre(request):
    ProsceniumTheatreParticipantFormSet = formset_factory(
        ProsceniumTheatreParticipantForm, formset=BaseProsceniumParticipantFormSet)
    registration = ProsceniumTheatreRegistration()

    context = {
        'registration_form': ProsceniumTheatreRegistrationForm(),
        'participant_formset': ProsceniumTheatreParticipantFormSet(),
    }

    if request.method == 'POST':
        registration_form = ProsceniumTheatreRegistrationForm(
            request.POST, request.FILES)
        participant_formset = ProsceniumTheatreParticipantFormSet(
            request.POST, request.FILES)

        context = {
            'registration_form': registration_form,
            'participant_formset': participant_formset,
        }

        if registration_form.is_valid() and participant_formset.is_valid():
            registration.institution = registration_form.cleaned_data.get(
                'institution')
            registration.contact1 = registration_form.cleaned_data.get(
                'contact1')
            registration.contact2 = registration_form.cleaned_data.get(
                'contact2')
            registration.email = registration_form.cleaned_data.get('email')
            registration.language = registration_form.cleaned_data.get(
                'language')
            registration.prelims_video = registration_form.cleaned_data.get(
                'prelims_video')
            registration.prelims_script = registration_form.cleaned_data.get(
                'prelims_script')
            try:
                registration.save()
            except IntegrityError:
                return render(request, "proscenium_theatre.html", {**context, **{'error_message': "Possible Duplicate Registration. Please retry."}})

            participants = []
            for participant_form in participant_formset:
                name = participant_form.cleaned_data.get('name')
                age = participant_form.cleaned_data.get('age')
                role = participant_form.cleaned_data.get('role')

                if name and age and role:
                    participants.append(ProsceniumTheatreParticipant(
                        registration_entry=registration, name=name, age=age, role=role))

            print(participants)
            try:
                with transaction.atomic():
                    ProsceniumTheatreParticipant.objects.filter(
                        registration_entry=registration).delete()
                    ProsceniumTheatreParticipant.objects.bulk_create(
                        participants)
                return redirect("http://pravega.org/pros.html")
            except IntegrityError:
                return render(request, "proscenium_theatre.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "proscenium_theatre.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        print('loading')
        return render(request, "proscenium_theatre.html", context)


def proscenium_streetplay(request):
    ProsceniumStreetPlayParticipantFormSet = formset_factory(
        ProsceniumStreetPlayParticipantForm, formset=BaseProsceniumParticipantFormSet)
    registration = ProsceniumStreetPlayRegistration()

    context = {
        'registration_form': ProsceniumStreetPlayRegistrationForm(),
        'participant_formset': ProsceniumStreetPlayParticipantFormSet(),
    }
    if request.method == 'POST':
        registration_form = ProsceniumStreetPlayRegistrationForm(
            request.POST, request.FILES)
        participant_formset = ProsceniumStreetPlayParticipantFormSet(
            request.POST, request.FILES)

        context = {
            'registration_form': registration_form,
            'participant_formset': participant_formset,
        }

        if registration_form.is_valid() and participant_formset.is_valid():
            registration.institution = registration_form.cleaned_data.get(
                'institution')
            registration.contact1 = registration_form.cleaned_data.get(
                'contact1')
            registration.contact2 = registration_form.cleaned_data.get(
                'contact2')
            registration.email = registration_form.cleaned_data.get('email')
            registration.language = registration_form.cleaned_data.get(
                'language')
            try:
                registration.save()
            except IntegrityError:
                return render(request, "proscenium_streetplay.html", {**context, **{'error_message': "Possible Duplicate Registration. Please retry."}})

            participants = []
            for participant_form in participant_formset:
                name = participant_form.cleaned_data.get('name')
                age = participant_form.cleaned_data.get('age')
                role = participant_form.cleaned_data.get('role')
                photo = participant_form.cleaned_data.get('photo')
                if name and age and role and photo:
                    participants.append(ProsceniumStreetPlayParticipant(
                        registration_entry=registration, name=name, age=age, role=role, photo=photo))
            try:
                with transaction.atomic():
                    ProsceniumStreetPlayParticipant.objects.filter(
                        registration_entry=registration).delete()
                    ProsceniumStreetPlayParticipant.objects.bulk_create(
                        participants)
                return redirect("http://pravega.org/pros.html")
            except IntegrityError:
                return render(request, "proscenium_streetplay.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "proscenium_streetplay.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "proscenium_streetplay.html", context)


def bob(request):
    BoBParticipantFormSet = formset_factory(
        BoBParticipantForm, formset=BaseBoBParticipantFormSet)
    registration = BoBRegistration()

    context = {
        'registration_form': BoBRegistrationForm(),
        'participant_formset': BoBParticipantFormSet(),
    }

    if request.method == 'POST':
        registration_form = BoBRegistrationForm(
            request.POST, request.FILES)
        participant_formset = BoBParticipantFormSet(
            request.POST, request.FILES)

        context = {
            'registration_form': registration_form,
            'participant_formset': participant_formset,
        }

        if registration_form.is_valid() and participant_formset.is_valid():
            registration.band_name = registration_form.cleaned_data.get(
                'band_name')
            registration.city = registration_form.cleaned_data.get(
                'city')
            registration.prelims_venue = registration_form.cleaned_data.get(
                'prelims_venue')
            registration.email = registration_form.cleaned_data.get('email')
            registration.genre = registration_form.cleaned_data.get(
                'genre')
            registration.audio_sample = registration_form.cleaned_data.get(
                'audio_sample')
            registration.facebook_link = registration_form.cleaned_data.get(
                'facebook_link')
            try:
                registration.save()
            except IntegrityError:
                return render(request, "bob.html", {**context, **{'error_message': "Possible Duplicate Registration. Please retry."}})

            participants = []
            for participant_form in participant_formset:
                name = participant_form.cleaned_data.get('name')
                contact = participant_form.cleaned_data.get('contact')
                instrument = participant_form.cleaned_data.get('instrument')
                if name and contact and instrument:
                    participants.append(BoBParticipant(
                        registration_entry=registration, name=name, contact=contact, instrument=instrument))

            try:
                with transaction.atomic():
                    BoBParticipant.objects.filter(
                        registration_entry=registration).delete()
                    BoBParticipant.objects.bulk_create(participants)
                return redirect("http://pravega.org/bob.html")
            except IntegrityError:
                return render(request, "bob.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "bob.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "bob.html", context)
