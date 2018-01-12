import os
import re
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now
from django.utils.safestring import mark_safe
from django.conf import settings
from .customfields import PhoneNumberField

IMAGE_FILE_VALIDATOR = FileExtensionValidator(
    allowed_extensions=['jpg', 'png'])
SCRIPT_FILE_VALIDATOR = FileExtensionValidator(
    allowed_extensions=['pdf', 'doc', 'docx', 'txt'])
VIDEO_FILE_VALIDATOR = FileExtensionValidator(
    allowed_extensions=['mp4', '3gp', 'mkv'])

THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT = 90, 120


def get_uploads_directory():
    if settings.MEDIA_ROOT:
        return settings.MEDIA_ROOT
    else:
        return "./uploads/"

def resolve_uploads_url(url):
    if settings.MEDIA_ROOT in url:
        return re.sub("/media.*?Pravega_2018", "", url)
    elif "/media/uploads/" in url:
        return re.sub("/media", "/cultural/uploads", url)
    else:
        return url

def image_preview(instance):
        if instance.photo:
            return mark_safe(f"<img src={resolve_uploads_url(instance.photo.url)} style=\"width:{THUMBNAIL_WIDTH}px; height:{THUMBNAIL_HEIGHT}px\"/>")
        else:
            return mark_safe("<p>No Photo</p>")

def file_download_link(file):
    if file:
        return mark_safe(f"<a href={resolve_uploads_url(file.url)} target=\"_blank\">Download</a>")
    else:
        return mark_safe("<p>Nothing to Download</p>")

class ProsceniumRegistration:
    ENGLISH = 'English'
    HINDI = 'Hindi'
    KANNADA = 'Kannada'
    LANGUAGES = ((ENGLISH, ENGLISH), (HINDI, HINDI), (KANNADA, KANNADA))


class ProsceniumParticipant:
    ACCOMPANIST = 'Accompanist'
    PERFORMER = 'Performer'
    ROLES = ((ACCOMPANIST, "Accompanist"), (PERFORMER, "Performer"))


class ProsceniumTheatreRegistration(models.Model):

    class Meta:
        unique_together = (("institution", "language"),)
    time = models.DateTimeField(default=now)
    referral_code = models.CharField(max_length=50, blank=True)
    institution = models.CharField(max_length=200)
    contact1 = PhoneNumberField.get_field()
    contact2 = PhoneNumberField.get_field(blank=True)
    email = models.EmailField()
    language = models.CharField(max_length=max(map(lambda x: len(x[0]), ProsceniumRegistration.LANGUAGES)),
                                choices=ProsceniumRegistration.LANGUAGES,
                                default=ProsceniumRegistration.ENGLISH)

    def upload_video_path(instance, filename):
        return os.path.join(get_uploads_directory(), f"theatre/videos/{instance.institution} - {instance.language} - {filename}")

    prelims_video = models.FileField(
        validators=[VIDEO_FILE_VALIDATOR],
        max_length=255,
        upload_to=upload_video_path,
        blank=True)
    
    prelims_video_link = models.URLField(blank=True)
    prelims_script_link = models.URLField(blank=True)
    
    def download_prelims_video(instance):
        return file_download_link(instance.prelims_video)

    def upload_script_path(instance, filename):
        return os.path.join(get_uploads_directory(), f"theatre/scripts/{instance.institution} - {instance.language} - {filename}")

    prelims_script = models.FileField(
        validators=[SCRIPT_FILE_VALIDATOR],
        max_length=255,
        upload_to=upload_script_path,
        blank=True)

    def download_prelims_script(instance):
        return file_download_link(instance.prelims_script)

    def __str__(self):
        return f"Institution: {self.institution}, Language: {self.language}, 1st Contact No.: {self.contact1}, 2nd Contact No.: {self.contact2}, E-Mail ID: {self.email}"


class ProsceniumTheatreParticipant(models.Model):
    registration_entry = models.ForeignKey(
        ProsceniumTheatreRegistration, on_delete=models.CASCADE)
    role = models.CharField(max_length=max(map(lambda x: len(x[0]), ProsceniumParticipant.ROLES)),
                            choices=ProsceniumParticipant.ROLES,
                            default=ProsceniumParticipant.PERFORMER)
    age = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=200)

    def upload_path(instance, filename):
        return os.path.join(get_uploads_directory(), f"theatre/participant_photos/{instance.registration_entry.institution} - {instance.registration_entry.language}/{instance.name} - {filename}")

    photo = models.ImageField(
        validators=[IMAGE_FILE_VALIDATOR],
        max_length=255,
        upload_to=upload_path,
        blank=True)

    photo_preview = image_preview

    def __str__(self):
        return f"Registration Entry: {self.registration_entry}, Name: {self.name}, Age: {self.age}, Role: {self.role}"


class ProsceniumStreetPlayRegistration(models.Model):

    class Meta:
        unique_together = (("institution", "language"),)
    time = models.DateTimeField(default=now)
    referral_code = models.CharField(max_length=50, blank=True)
    institution = models.CharField(max_length=200)
    contact1 = PhoneNumberField.get_field()
    contact2 = PhoneNumberField.get_field(blank=True)
    email = models.EmailField()
    language = models.CharField(max_length=max(map(lambda x: len(x[0]), ProsceniumRegistration.LANGUAGES)),
                                choices=ProsceniumRegistration.LANGUAGES,
                                default=ProsceniumRegistration.ENGLISH)

    def __str__(self):
        return f"Institution: {self.institution}, Language: {self.language}, 1st Contact No.: {self.contact1}, 2nd Contact No.: {self.contact2}, E-Mail ID: {self.email}"


class ProsceniumStreetPlayParticipant(models.Model):
    registration_entry = models.ForeignKey(
        ProsceniumStreetPlayRegistration, on_delete=models.CASCADE)
    role = models.CharField(max_length=max(map(lambda x: len(x[0]), ProsceniumParticipant.ROLES)),
                            choices=ProsceniumParticipant.ROLES,
                            default=ProsceniumParticipant.PERFORMER)
    age = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=200)

    def upload_path(instance, filename):
        return os.path.join(get_uploads_directory(), f"street_play/participant_photos/{instance.registration_entry.institution} - {instance.registration_entry.language}/{instance.name} - {filename}")

    photo = models.ImageField(
        validators=[IMAGE_FILE_VALIDATOR],
        max_length=255,
        upload_to=upload_path,
        blank=True)

    photo_preview = image_preview

    def __str__(self):
        return f"Registration Entry: {self.registration_entry}, Name: {self.name}, Age: {self.age}, Role: {self.role}"


class BoBRegistration(models.Model):

    class Meta:
        unique_together = (("band_name", "city", "genre"),)

    AUDIO_FILE_VALIDATOR = FileExtensionValidator(
        allowed_extensions=['mp3', 'wav'])
    BANGALORE = "Bangalore"
    KOLKATA = "Kolkata"
    CHENNAI = "Chennai"
    DELHI = "Delhi"
    MUMBAI = "Mumbai"
    PRELIMS_VENUES = ((BANGALORE, BANGALORE), (KOLKATA, KOLKATA),
                      (CHENNAI, CHENNAI), (DELHI, DELHI), (MUMBAI, MUMBAI))
    time = models.DateTimeField(default=now)
    referral_code = models.CharField(max_length=50, blank=True)
    band_name = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    city = models.CharField(max_length=200)
    facebook_link = models.URLField(blank=True)

    def upload_path(instance, filename):
        return os.path.join(get_uploads_directory(), f"bob/audio/{instance.band_name} - {instance.city} - {filename}")

    audio_sample_file = models.FileField(
        validators=[AUDIO_FILE_VALIDATOR],
        max_length=255,
        upload_to=upload_path, blank=True)

    def download_audio_sample_file(instance):
        return file_download_link(instance.audio_sample_file)
    
    audio_sample_link = models.URLField(blank=True)

    prelims_venue = models.CharField(max_length=max(map(lambda x: len(x[0]), PRELIMS_VENUES)),
                                     choices=PRELIMS_VENUES,
                                     default=BANGALORE)

    def __str__(self):
        return f"Band Name: {self.band_name}, City: {self.city}, Genre: {self.genre}, Prelims Venue: {self.prelims_venue}, E-Mail ID: {self.email}"


class BoBParticipant(models.Model):
    registration_entry = models.ForeignKey(
        BoBRegistration, on_delete=models.CASCADE)
    instrument = models.CharField(max_length=200)
    contact = PhoneNumberField.get_field()
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"Registration Entry: {self.registration_entry}, Name: {self.name}, Contact: {self.contact}, Instrument: {self.instrument}"


class LasyaRegistration(models.Model):

    class Meta:
        unique_together = (("name", "institution"),)
    time = models.DateTimeField(default=now)
    referral_code = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=200, unique=True)
    institution = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    contact = PhoneNumberField.get_field()

    def upload_video_path(instance, filename):
        return os.path.join(get_uploads_directory(), f"lasya_prelims/videos/{instance.name} - {instance.institution} - {filename}")

    prelims_video = models.FileField(
        validators=[VIDEO_FILE_VALIDATOR],
        max_length=255,
        blank=True,
        upload_to=upload_video_path)
    
    def download_prelims_video(instance):
        return file_download_link(instance.prelims_video)

    prelims_video_link = models.URLField(blank=True)

    def __str__(self):
        return f"Team Name: {self.name}, Institution: {self.institution}, E-Mail ID: {self.email}, Contact No.: {self.contact}"


class LasyaParticipant(models.Model):
    registration_entry = models.ForeignKey(
        LasyaRegistration, on_delete=models.CASCADE)
    contact = PhoneNumberField.get_field()
    email = models.EmailField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"Registration Entry: {self.registration_entry}, Name: {self.name}, Contact: {self.contact}, E-Mail ID: {self.email}"


class SInECRegistration(models.Model):

    class Meta:
        unique_together = (("team_name", "project_name"),)
    time = models.DateTimeField(default=now)
    referral_code = models.CharField(max_length=50, blank=True)
    team_name = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    email = models.EmailField()
    contact = PhoneNumberField.get_field()
    address = models.CharField(max_length=400)
    project_abstract = models.TextField()
    project_field = models.CharField(max_length=200)
    project_patented = models.BooleanField()
    registered_company = models.BooleanField()

    PUBLIC = "Available for Public Awareness"
    PRIVATE = "Unavailable for Public Awareness, Closed Room Presentation and Evaluation"
    PRIVACY_PREFERENCES = (
        (PUBLIC, "I would like to display my project to the general public to improve awareness about my project."),
        (PRIVATE, "I would like my project to be presented and evaluated in a closed room and would not like to display it to the general public."),)
    privacy_preference = models.CharField(max_length=max(map(lambda x: len(x[0]), PRIVACY_PREFERENCES)),
                                          choices=PRIVACY_PREFERENCES,
                                          default=PRIVATE)

    def upload_path(instance, filename):
        return os.path.join(get_uploads_directory(), f"sinec/project_files/{instance.team_name} - {instance.project_name} - {filename}")

    def upload_video_path(instance, filename):
        return os.path.join(get_uploads_directory(), f"sinec/project_files/video/{instance.team_name} - {instance.project_name} - {filename}")

    project_file = models.FileField(
        max_length=255,
        upload_to=upload_path,
        blank=True)

    def download_project_file(instance):
        return file_download_link(instance.project_file)

    project_video = models.FileField(
        max_length=255,
        upload_to=upload_video_path,
        blank=True)

    project_video_link = models.URLField(blank=True)

    def download_project_video(instance):
        return file_download_link(instance.project_video)

    def __str__(self):
        return f"Team Name: {self.team_name}, Project Name: {self.project_name}, E-Mail ID: {self.email}, Contact No.: {self.contact}"


class SInECParticipant(models.Model):
    registration_entry = models.ForeignKey(
        SInECRegistration, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    UG = "UG"
    MASTERS = "Masters"
    PHD = "Ph.D."
    POST_DOC = "Post-Doc"
    STUDENT_TYPES = ((UG, UG), (MASTERS, MASTERS),
                     (PHD, PHD), (POST_DOC, POST_DOC),)

    student_type = models.CharField(max_length=max(map(lambda x: len(x[0]), STUDENT_TYPES)),
                                    choices=STUDENT_TYPES,
                                    default=UG)

    def __str__(self):
        return f"Registration Entry: {self.registration_entry}, Name: {self.name}, Type: {self.student_type}, Institution: {self.institution}, City: {self.city}"


class DecoherenceRegistration(models.Model):
    time = models.DateTimeField(default=now)
    referral_code = models.CharField(max_length=50, blank=True)
    team_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"Team Name: {self.team_name}"


class DecoherenceParticipant(models.Model):
    registration_entry = models.ForeignKey(
        DecoherenceRegistration, on_delete=models.CASCADE)
    contact = PhoneNumberField.get_field()
    email = models.EmailField()
    name = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)

    def __str__(self):
        return f"Registration Entry: {self.registration_entry}, Name: {self.name}, Contact: {self.contact}, E-Mail ID: {self.email}"

class OpenMicRegistration(models.Model):

    class Meta:
        unique_together = (("email", "name", "event"),)

    time = models.DateTimeField(default=now)
    referral_code = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=200)
    event = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    expected_performance_duration_mins = models.PositiveSmallIntegerField()
    instrument_requirement = models.CharField(max_length=200, blank=True)
    reason_for_gt_3_members = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return f"Name: {self.name}, Event: {self.event}, E-Mail ID: {self.email}, Expected Performance Duration: {self.expected_performance_duration_mins} minutes"


class OpenMicParticipant(models.Model):
    registration_entry = models.ForeignKey(
        OpenMicRegistration, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"Registration Entry: {self.registration_entry}, Name: {self.name}"


class HackathonRegistration(models.Model):
    time = models.DateTimeField(default=now)
    referral_code = models.CharField(max_length=50, blank=True)
    team_name = models.CharField(max_length=200, unique=True)
    contact = PhoneNumberField.get_field()
    email = models.EmailField()
    abstract = models.TextField()

    def __str__(self):
        return f"Team Name: {self.team_name}, Contact: {self.contact}, E-Mail ID: {self.email}"


class HackathonParticipant(models.Model):
    registration_entry = models.ForeignKey(
        HackathonRegistration, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"Registration Entry: {self.registration_entry}, Name: {self.name}"
