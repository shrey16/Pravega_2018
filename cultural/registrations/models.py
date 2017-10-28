from django.db import models
from django.core.validators import FileExtensionValidator
from .customfields import PhoneNumberField

IMAGE_FILE_VALIDATOR = FileExtensionValidator(
    allowed_extensions=['jpg', 'png'])
SCRIPT_FILE_VALIDATOR = FileExtensionValidator(
    allowed_extensions=['pdf', 'doc', 'docx', 'txt'])
VIDEO_FILE_VALIDATOR = FileExtensionValidator(
    allowed_extensions=['mp4', '3gp', 'mkv'])


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
    time = models.DateTimeField(auto_now_add=True)
    institution = models.CharField(max_length=200)
    contact1 = PhoneNumberField.get_field()
    contact2 = PhoneNumberField.get_field(blank=True)
    email = models.EmailField()
    language = models.CharField(max_length=max(map(lambda x: len(x[0]), ProsceniumRegistration.LANGUAGES)),
                                choices=ProsceniumRegistration.LANGUAGES,
                                default=ProsceniumRegistration.ENGLISH)

    def upload_video_path(instance, filename):
        return f"./uploads/theatre_prelims/videos/{instance.institution} - {instance.language} - {filename}"

    prelims_video = models.FileField(
        validators=[VIDEO_FILE_VALIDATOR],
        max_length=255,
        upload_to=upload_video_path)

    def upload_script_path(instance, filename):
        return f"./uploads/theatre_prelims/scripts/{instance.institution} - {instance.language} - {filename}"

    prelims_script = models.FileField(
        validators=[SCRIPT_FILE_VALIDATOR],
        max_length=255,
        upload_to=upload_script_path)

    def __str__(self):
        return f"Institution: {self.institution}, Language: {self.language}, 1st Contact No.: {self.contact1}, 2nd Contact No.: {self.contact2}, E-Mail ID: {self.email}"


class ProsceniumTheatreParticipant(models.Model):
    registration_entry = models.ForeignKey(
        ProsceniumTheatreRegistration, on_delete=models.CASCADE)
    role = models.CharField(max_length=max(map(lambda x: len(x[0]), ProsceniumParticipant.ROLES)),
                            choices=ProsceniumParticipant.ROLES,
                            default=ProsceniumParticipant.PERFORMER)
    age = models.IntegerField()
    name = models.CharField(max_length=200)

    def upload_path(instance, filename):
        return f"./uploads/theatre/participant_photos/{instance.registration_entry.institution} - {instance.registration_entry.language}/{instance.name} - {filename}"

    photo = models.ImageField(
        validators=[IMAGE_FILE_VALIDATOR],
        max_length=255,
        upload_to=upload_path)

    def __str__(self):
        return f"Registration Entry: {self.registration_entry}, Name: {self.name}, Age: {self.age}, Role: {self.role}"


class ProsceniumStreetPlayRegistration(models.Model):

    class Meta:
        unique_together = (("institution", "language"),)
    time = models.DateTimeField(auto_now_add=True)
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
    age = models.IntegerField()
    name = models.CharField(max_length=200)

    def upload_path(instance, filename):
        return f"./uploads/street_play/participant_photos/{instance.registration_entry.institution} - {instance.registration_entry.language}/{instance.name} - {filename}"

    photo = models.ImageField(
        validators=[IMAGE_FILE_VALIDATOR],
        max_length=255,
        upload_to=upload_path)

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
    time = models.DateTimeField(auto_now_add=True)
    band_name = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    city = models.CharField(max_length=200)
    facebook_link = models.URLField(blank=True)

    def upload_path(instance, filename):
        return f"./uploads/bob/audio/{instance.band_name} - {instance.city} - {filename}"

    audio_sample_file = models.FileField(
        validators=[AUDIO_FILE_VALIDATOR],
        max_length=255,
        upload_to=upload_path, blank=True)
    audio_sample_link = models.URLField(blank=True)

    prelims_venue = models.CharField(max_length=max(map(lambda x: len(x[0]), PRELIMS_VENUES)),
                                     choices=PRELIMS_VENUES,
                                     default=BANGALORE)

    def __str__(self):
        return f"Band Name: {self.band_name}, City: {self.city} Genre: {self.genre}, Prelims Venue: {self.prelims_venue}, E-Mail ID: {self.email}"


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
    time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, unique=True)
    institution = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    contact = PhoneNumberField.get_field()

    def upload_video_path(instance, filename):
        return f"./uploads/lasya_prelims/videos/{instance.name} - {instance.institution} - {filename}"

    prelims_video = models.FileField(
        validators=[VIDEO_FILE_VALIDATOR],
        max_length=255,
        upload_to=upload_video_path)

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
    time = models.DateTimeField(auto_now_add=True)
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
    PRIVATE = "Unavailabable for Public Awareness, Closed Room Presentation and Evaluation"
    PRIVACY_PREFERENCES = (
        (PUBLIC, "I would like my project to be presented and evaluated in a closed room and would not like to display it to the general public."),
        (PRIVATE, "I would like to display my project to the general public to improve awareness about my project."),)
    privacy_preference = models.CharField(max_length=max(map(lambda x: len(x[0]), PRIVACY_PREFERENCES)),
                                          choices=PRIVACY_PREFERENCES,
                                          default=PRIVATE)

    def upload_video_path(instance, filename):
        return f"./uploads/sinec/project_files/{instance.team_name} - {instance.project_name} - {filename}"

    project_file = models.FileField(
        max_length=255,
        upload_to=upload_video_path)

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
