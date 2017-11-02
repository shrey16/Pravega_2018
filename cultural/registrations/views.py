from django.shortcuts import render, redirect
from django.db import IntegrityError, transaction
from django.forms.formsets import formset_factory
from .forms import *
from .models import *


def root(request):
    return redirect("registrations/")


def index(request):
    return render(request, "index.html", {})


def proscenium_theatre(request):
    ProsceniumTheatreParticipantFormSet = formset_factory(
        ProsceniumTheatreParticipantForm, formset=BaseProsceniumParticipantFormSet, min_num=1, validate_min=True, max_num=10, validate_max=True, extra=3)
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
                photo = participant_form.cleaned_data.get('photo')

                if name and age and role and photo:
                    participants.append(ProsceniumTheatreParticipant(
                        registration_entry=registration, name=name, age=age, role=role, photo=photo))
            try:
                with transaction.atomic():
                    ProsceniumTheatreParticipant.objects.filter(
                        registration_entry=registration).delete()
                    ProsceniumTheatreParticipant.objects.bulk_create(
                        participants)
                return render(request, "success.html", {'event_name': 'Proscenium'})
            except IntegrityError:
                return render(request, "proscenium_theatre.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "proscenium_theatre.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "proscenium_theatre.html", context)


def proscenium_streetplay(request):
    ProsceniumStreetPlayParticipantFormSet = formset_factory(
        ProsceniumStreetPlayParticipantForm, formset=BaseProsceniumParticipantFormSet, min_num=1, validate_min=True, max_num=10, validate_max=True, extra=3)
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
                return render(request, "success.html", {'event_name': 'Footprints'})
            except IntegrityError:
                return render(request, "proscenium_streetplay.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "proscenium_streetplay.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "proscenium_streetplay.html", context)


def bob(request):
    BoBParticipantFormSet = formset_factory(
        BoBParticipantForm, formset=BaseBoBParticipantFormSet, min_num=3, validate_min=True, extra=0)
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
            registration.audio_sample_file = registration_form.cleaned_data.get(
                'audio_sample_file')
            registration.audio_sample_link = registration_form.cleaned_data.get(
                'audio_sample_link')
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
                return render(request, "success.html", {'event_name': 'Battle of Bands'})
            except IntegrityError:
                return render(request, "bob.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "bob.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "bob.html", context)


def lasya(request):
    LasyaParticipantFormSet = formset_factory(
        LasyaParticipantForm, formset=BaseLasyaParticipantFormSet, min_num=5, validate_min=True, max_num=20, validate_max=True, extra=0)
    registration = LasyaRegistration()

    context = {
        'registration_form': LasyaRegistrationForm(),
        'participant_formset': LasyaParticipantFormSet(),
    }

    if request.method == 'POST':
        registration_form = LasyaRegistrationForm(
            request.POST, request.FILES)
        participant_formset = LasyaParticipantFormSet(
            request.POST, request.FILES)

        context = {
            'registration_form': registration_form,
            'participant_formset': participant_formset,
        }

        if registration_form.is_valid() and participant_formset.is_valid():
            registration.name = registration_form.cleaned_data.get('name')
            registration.email = registration_form.cleaned_data.get('email')
            registration.contact = registration_form.cleaned_data.get(
                'contact')
            registration.prelims_video = registration_form.cleaned_data.get(
                'prelims_video')
            registration.institution = registration_form.cleaned_data.get(
                'institution')
            try:
                registration.save()
            except IntegrityError:
                return render(request, "lasya.html", {**context, **{'error_message': "Possible Duplicate Registration. Please retry."}})

            participants = []
            for participant_form in participant_formset:
                name = participant_form.cleaned_data.get('name')
                contact = participant_form.cleaned_data.get('contact')
                email = participant_form.cleaned_data.get('email')
                if name and contact and email:
                    participants.append(LasyaParticipant(
                        registration_entry=registration, name=name, contact=contact, email=email))

            try:
                with transaction.atomic():
                    LasyaParticipant.objects.filter(
                        registration_entry=registration).delete()
                    LasyaParticipant.objects.bulk_create(participants)
                return render(request, "success.html", {'event_name': 'Lasya'})
            except IntegrityError:
                return render(request, "lasya.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "lasya.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "lasya.html", context)


def sinec(request):
    SInECParticipantFormSet = formset_factory(
        SInECParticipantForm, formset=BaseSInECParticipantFormSet, min_num=1, validate_min=True, extra=3)
    registration = SInECRegistration()

    context = {
        'registration_form': SInECRegistrationForm(),
        'participant_formset': SInECParticipantFormSet(),
    }

    if request.method == 'POST':
        registration_form = SInECRegistrationForm(
            request.POST, request.FILES)
        participant_formset = SInECParticipantFormSet(
            request.POST, request.FILES)

        context = {
            'registration_form': registration_form,
            'participant_formset': participant_formset,
        }

        if registration_form.is_valid() and participant_formset.is_valid():
            registration.team_name = registration_form.cleaned_data.get(
                'team_name')
            registration.project_name = registration_form.cleaned_data.get(
                'project_name')
            registration.project_field = registration_form.cleaned_data.get(
                'project_field')
            registration.project_abstract = registration_form.cleaned_data.get(
                'project_abstract')
            registration.project_patented = registration_form.cleaned_data.get(
                'project_patented')
            registration.registered_company = registration_form.cleaned_data.get(
                'registered_company')
            registration.privacy_preference = registration_form.cleaned_data.get(
                'privacy_preference')
            registration.email = registration_form.cleaned_data.get('email')
            registration.contact = registration_form.cleaned_data.get(
                'contact')
            registration.address = registration_form.cleaned_data.get(
                'address')
            registration.project_file = registration_form.cleaned_data.get(
                'project_file')

            try:
                registration.save()
            except IntegrityError:
                return render(request, "pis.html", {**context, **{'error_message': "Possible Duplicate Registration. Please retry."}})

            participants = []
            for participant_form in participant_formset:
                name = participant_form.cleaned_data.get('name')
                city = participant_form.cleaned_data.get('city')
                student_type = participant_form.cleaned_data.get(
                    'student_type')
                institution = participant_form.cleaned_data.get('institution')
                if name and city and student_type and institution:
                    participants.append(SInECParticipant(
                        registration_entry=registration, name=name, student_type=student_type, city=city, institution=institution))

            try:
                with transaction.atomic():
                    SInECParticipant.objects.filter(
                        registration_entry=registration).delete()
                    SInECParticipant.objects.bulk_create(participants)
                return render(request, "success.html", {'event_name': 'Pravega Innovation Summit'})
            except IntegrityError:
                return render(request, "pis.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "pis.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "pis.html", context)
