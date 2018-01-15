from django.shortcuts import render
from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.forms.formsets import formset_factory
from .forms import *
from .models import *


def index(request):
    return render(request, "index.html", {})


def proscenium_theatre(request):
    ProsceniumTheatreParticipantFormSet = formset_factory(
        ProsceniumTheatreParticipantForm, formset=BaseProsceniumParticipantFormSet, min_num=1, validate_min=True, max_num=13, extra=3)
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
            registration.referral_code = registration_form.cleaned_data.get(
                'referral_code')
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
            registration.prelims_video_link = registration_form.cleaned_data.get(
                'prelims_video_link')
            registration.prelims_script = registration_form.cleaned_data.get(
                'prelims_script')
            registration.prelims_script_link = registration_form.cleaned_data.get(
                'prelims_script_link')
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

                if name and age and role:
                    participants.append(ProsceniumTheatreParticipant(
                        registration_entry=registration, name=name, age=age, role=role, photo=photo))
            try:
                with transaction.atomic():
                    ProsceniumTheatreParticipant.objects.filter(
                        registration_entry=registration).delete()
                    ProsceniumTheatreParticipant.objects.bulk_create(
                        participants)
                return render(request, "success.html", {'event_name': 'Proscenium', 'id': registration.id})
            except IntegrityError:
                return render(request, "proscenium_theatre.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "proscenium_theatre.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "proscenium_theatre.html", context)


def proscenium_theatre_video(request):
    context = {'registration_form': ProsceniumTheatreVideoSubmissionForm()}
    if request.method == 'POST':
        registration_form = ProsceniumTheatreVideoSubmissionForm(
            request.POST, request.FILES)
        context = {'registration_form': registration_form}
        if registration_form.is_valid():
            index = registration_form.cleaned_data.get('index')
            try:
                registration = ProsceniumTheatreRegistration.objects.get(
                    pk=index)
                if (registration.prelims_video or registration.prelims_video_link) and (registration.prelims_script or registration.prelims_script_link):
                    return render(request, "proscenium_video_submission.html", {**context, **{'error_message': "Video and Script have already been submitted. Re-submission is not allowed."}})
                else:
                    registration.prelims_video = registration_form.cleaned_data.get(
                        'prelims_video')
                    registration.prelims_video_link = registration_form.cleaned_data.get(
                        'prelims_video_link')
                    registration.prelims_script = registration_form.cleaned_data.get(
                        'prelims_script')
                    registration.prelims_script_link = registration_form.cleaned_data.get(
                        'prelims_script_link')
            except ObjectDoesNotExist:
                return render(request, "proscenium_video_submission.html", {**context, **{'error_message': "Unrecognized Registration ID. Please retry."}})
            try:
                registration.save()
                return render(request, "success.html", {'event_name': 'Proscenium Prelims Video Submission', 'id': registration.id})
            except IntegrityError:
                return render(request, "proscenium_video_submission.html", {**context, **{'error_message': "Possible Duplicate Registration. Please retry."}})
        else:
            return render(request, "proscenium_video_submission.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "proscenium_video_submission.html", context)


def proscenium_streetplay(request):
    ProsceniumStreetPlayParticipantFormSet = formset_factory(
        ProsceniumStreetPlayParticipantForm, formset=BaseProsceniumStreetPlayParticipantFormSet, min_num=1, validate_min=True, max_num=20, extra=3)
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
            registration.referral_code = registration_form.cleaned_data.get(
                'referral_code')
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
                if name and age and role:
                    participants.append(ProsceniumStreetPlayParticipant(
                        registration_entry=registration, name=name, age=age, role=role, photo=photo))
            try:
                with transaction.atomic():
                    ProsceniumStreetPlayParticipant.objects.filter(
                        registration_entry=registration).delete()
                    ProsceniumStreetPlayParticipant.objects.bulk_create(
                        participants)
                return render(request, "success.html", {'event_name': 'Footprints', 'id': registration.id})
            except IntegrityError:
                return render(request, "proscenium_streetplay.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "proscenium_streetplay.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "proscenium_streetplay.html", context)


def bob(request):
    BoBParticipantFormSet = formset_factory(
        BoBParticipantForm, formset=BaseBoBParticipantFormSet, min_num=3, extra=0)
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
            registration.referral_code = registration_form.cleaned_data.get(
                'referral_code')
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
                return render(request, "success.html", {'event_name': 'Battle of Bands', 'id': registration.id})
            except IntegrityError:
                return render(request, "bob.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "bob.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "bob.html", context)


def lasya(request):
    LasyaParticipantFormSet = formset_factory(
        LasyaParticipantForm, formset=BaseLasyaParticipantFormSet, min_num=5, max_num=20, extra=0)
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
            registration.referral_code = registration_form.cleaned_data.get(
                'referral_code')
            registration.name = registration_form.cleaned_data.get('name')
            registration.email = registration_form.cleaned_data.get('email')
            registration.contact = registration_form.cleaned_data.get(
                'contact')
            registration.prelims_video = registration_form.cleaned_data.get(
                'prelims_video')
            registration.prelims_video_link = registration_form.cleaned_data.get(
                'prelims_video_link')
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
                return render(request, "success.html", {'event_name': 'Lasya', 'id': registration.id})
            except IntegrityError:
                return render(request, "lasya.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "lasya.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "lasya.html", context)


def lasya_video(request):
    context = {'registration_form': LasyaVideoSubmissionForm()}
    if request.method == 'POST':
        registration_form = LasyaVideoSubmissionForm(
            request.POST, request.FILES)
        context = {'registration_form': registration_form}
        if registration_form.is_valid():
            index = registration_form.cleaned_data.get('index')
            try:
                registration = LasyaRegistration.objects.get(
                    pk=index)
                if registration.prelims_video:
                    return render(request, "lasya_video_submission.html", {**context, **{'error_message': "Video has already been submitted. Re-submission is not allowed."}})
                else:
                    registration.prelims_video = registration_form.cleaned_data.get(
                        'prelims_video')
            except ObjectDoesNotExist:
                return render(request, "lasya_video_submission.html", {**context, **{'error_message': "Unrecognized Registration ID. Please retry."}})
            try:
                registration.save()
                return render(request, "success.html", {'event_name': 'Lasya Prelims Video Submission', 'id': registration.id})
            except IntegrityError:
                return render(request, "lasya_video_submission.html", {**context, **{'error_message': "Possible Duplicate Registration. Please retry."}})
        else:
            return render(request, "lasya_video_submission.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "lasya_video_submission.html", context)


def pis(request):
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
            registration.referral_code = registration_form.cleaned_data.get(
                'referral_code')
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
                return render(request, "success.html", {'event_name': 'Pravega Innovation Summit', 'id': registration.id})
            except IntegrityError:
                return render(request, "pis.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "pis.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "pis.html", context)


def pis_video(request):
    context = {'registration_form': PisVideoSubmissionForm()}
    if request.method == 'POST':
        registration_form = PisVideoSubmissionForm(
            request.POST, request.FILES)
        context = {'registration_form': registration_form}
        if registration_form.is_valid():
            index = registration_form.cleaned_data.get('index')
            try:
                registration = SInECRegistration.objects.get(
                    pk=index)
                if registration.project_video:
                    return render(request, "pis_video.html", {**context, **{'error_message': "Video has already been submitted. Re-submission is not allowed."}})
                else:
                    registration.project_video = registration_form.cleaned_data.get(
                        'project_video')
                if registration.project_video_link:
                    return render(request, "pis_video.html", {**context, **{'error_message': "Link to Video has already been submitted. Re-submission is not allowed."}})
                else:
                    registration.project_video_link = registration_form.cleaned_data.get(
                        'project_video_link')
            except ObjectDoesNotExist:
                return render(request, "pis_video.html", {**context, **{'error_message': "Unrecognized Registration ID. Please retry."}})
            try:
                registration.save()
                return render(request, "success.html", {'event_name': 'PIS Project Video Submission', 'id': registration.id})
            except IntegrityError:
                return render(request, "pis_video.html", {**context, **{'error_message': "Possible Duplicate Registration. Please retry."}})
        else:
            return render(request, "pis_video.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "pis_video.html", context)

def openmic(request):
    OpenMicParticipantFormSet = formset_factory(
        OpenMicParticipantForm, formset=BaseOpenMicParticipantFormSet, min_num=1, validate_min=True, extra=0)
    registration = OpenMicRegistration()

    context = {
        'registration_form': OpenMicRegistrationForm(),
        'participant_formset': OpenMicParticipantFormSet(),
    }

    if request.method == 'POST':
        participant_formset = OpenMicParticipantFormSet(
            request.POST, request.FILES)
        participant_count = len(list(filter(lambda form: form.is_valid(
        ), participant_formset.forms))) if participant_formset.is_valid() else 0
        registration_form = OpenMicRegistrationForm(
            request.POST, request.FILES, participant_count=participant_count)

        context = {
            'registration_form': registration_form,
            'participant_formset': participant_formset,
        }

        if registration_form.is_valid() and participant_formset.is_valid():
            registration.referral_code = registration_form.cleaned_data.get(
                'referral_code')
            registration.name = registration_form.cleaned_data.get(
                'name')
            registration.email = registration_form.cleaned_data.get('email')
            registration.event = registration_form.cleaned_data.get(
                'event')
            registration.expected_performance_duration_mins = registration_form.cleaned_data.get(
                'expected_performance_duration_mins')
            registration.instrument_requirement = registration_form.cleaned_data.get(
                'instrument_requirement')
            registration.reason_for_gt_3_members = registration_form.cleaned_data.get(
                'reason_for_gt_3_members')
            try:
                registration.save()
            except IntegrityError:
                return render(request, "openmic.html", {**context, **{'error_message': "Possible Duplicate Registration. Please retry."}})

            participants = []
            for participant_form in participant_formset:
                name = participant_form.cleaned_data.get('name')
                if name:
                    participants.append(OpenMicParticipant(
                        registration_entry=registration, name=name))

            try:
                with transaction.atomic():
                    OpenMicParticipant.objects.filter(
                        registration_entry=registration).delete()
                    OpenMicParticipant.objects.bulk_create(participants)
                return render(request, "success.html", {'event_name': 'Open Mic', 'id': registration.id})
            except IntegrityError:
                return render(request, "openmic.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "openmic.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "openmic.html", context)


def hackathon(request):
    HackathonParticipantFormSet = formset_factory(
        OpenMicParticipantForm, formset=BaseHackathonParticipantFormSet, min_num=1, validate_min=True, max_num=4, extra=1)
    registration = HackathonRegistration()

    context = {
        'registration_form': HackathonRegistrationForm(),
        'participant_formset': HackathonParticipantFormSet(),
    }

    if request.method == 'POST':
        participant_formset = HackathonParticipantFormSet(
            request.POST, request.FILES)
        registration_form = HackathonRegistrationForm(
            request.POST, request.FILES)

        context = {
            'registration_form': registration_form,
            'participant_formset': participant_formset,
        }

        if registration_form.is_valid() and participant_formset.is_valid():
            registration.referral_code = registration_form.cleaned_data.get(
                'referral_code')
            registration.team_name = registration_form.cleaned_data.get(
                'team_name')
            registration.email = registration_form.cleaned_data.get('email')
            registration.abstract = registration_form.cleaned_data.get(
                'abstract')
            registration.contact = registration_form.cleaned_data.get(
                'contact')

            try:
                registration.save()
            except IntegrityError:
                return render(request, "hackathon.html", {**context, **{'error_message': "Possible Duplicate Registration. Please retry."}})

            participants = []
            for participant_form in participant_formset:
                name = participant_form.cleaned_data.get('name')
                if name:
                    participants.append(HackathonParticipant(
                        registration_entry=registration, name=name))

            try:
                with transaction.atomic():
                    HackathonParticipant.objects.filter(
                        registration_entry=registration).delete()
                    HackathonParticipant.objects.bulk_create(participants)
                return render(request, "success.html", {'event_name': 'Hackathon', 'id': registration.id})
            except IntegrityError:
                return render(request, "hackathon.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "hackathon.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "hackathon.html", context)

def hackathon_abstract(request):
    context = {'registration_form': HackathonAbstractUpdateForm()}
    if request.method == 'POST':
        registration_form = HackathonAbstractUpdateForm(
            request.POST, request.FILES)
        context = {'registration_form': registration_form}
        if registration_form.is_valid():
            index = registration_form.cleaned_data.get('index')
            try:
                registration = HackathonRegistration.objects.get(
                    pk=index)
                registration.abstract = registration_form.cleaned_data.get(
                    'abstract')
            except ObjectDoesNotExist:
                return render(request, "hackathon_abstract.html", {**context, **{'error_message': "Unrecognized Registration ID. Please retry."}})
            try:
                registration.save()
                return render(request, "success.html", {'event_name': 'Hackathon Abstract Update', 'id': registration.id})
            except IntegrityError:
                return render(request, "hackathon_abstract.html", {**context, **{'error_message': "Possible Duplicate Registration. Please retry."}})
        else:
            return render(request, "hackathon_abstract.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "hackathon_abstract.html", context)

def decoherence(request):
    DecoherenceParticipantFormSet = formset_factory(
        DecoherenceParticipantForm, formset=BaseDecoherenceParticipantFormSet, min_num=1, max_num=2, validate_min=True, extra=1)
    registration = DecoherenceRegistration()

    context = {
        'registration_form': DecoherenceRegistrationForm(),
        'participant_formset': DecoherenceParticipantFormSet(),
    }

    if request.method == 'POST':
        participant_formset = DecoherenceParticipantFormSet(
            request.POST, request.FILES)
        registration_form = DecoherenceRegistrationForm(
            request.POST, request.FILES)

        context = {
            'registration_form': registration_form,
            'participant_formset': participant_formset,
        }

        if registration_form.is_valid() and participant_formset.is_valid():
            registration.referral_code = registration_form.cleaned_data.get(
                'referral_code')
            registration.team_name = registration_form.cleaned_data.get(
                'team_name')            
            try:
                registration.save()
            except IntegrityError:
                return render(request, "decoherence.html", {**context, **{'error_message': "Possible Duplicate Registration. Please retry."}})

            participants = []
            for participant_form in participant_formset:
                name = participant_form.cleaned_data.get('name')
                contact = participant_form.cleaned_data.get('contact')
                email = participant_form.cleaned_data.get('email')
                institution = participant_form.cleaned_data.get('institution')
                if name and contact and email and institution:
                    participants.append(DecoherenceParticipant(
                        registration_entry=registration, name=name, contact=contact, email=email, institution=institution))

            try:
                with transaction.atomic():
                    DecoherenceParticipant.objects.filter(
                        registration_entry=registration).delete()
                    DecoherenceParticipant.objects.bulk_create(participants)
                return render(request, "success.html", {'event_name': 'Decoherence', 'id': registration.id})
            except IntegrityError:
                return render(request, "decoherence.html", {**context, **{'error_message': "Error saving participant data. Please retry."}})
        else:
            return render(request, "decoherence.html", {**context, **{'error_message': "Check your input, it might be incorrect."}})
    else:
        return render(request, "decoherence.html", context)
