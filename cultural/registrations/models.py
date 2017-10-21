from django.db import models
from django.core.validators import FileExtensionValidator
from .customfields import PhoneNumberField

IMAGE_FILE_VALIDATOR = FileExtensionValidator(
    allowed_extensions=['jpg', 'png'])


class ProsceniumTheatreRegistration(models.Model):

    class Meta:
        unique_together = (("institution", "language"),)

    SCRIPT_FILE_VALIDATOR = FileExtensionValidator(
        allowed_extensions=['pdf', 'doc', 'docx', 'txt'])
    VIDEO_FILE_VALIDATOR = FileExtensionValidator(
        allowed_extensions=['mp4', '3gp', 'mkv'])
    ENGLISH = 'en'
    HINDI = 'hi'
    KANNADA = 'ka'
    LANGUAGES = ((ENGLISH, "English"), (HINDI, "Hindi"), (KANNADA, "Kannada"))
    institution = models.CharField(max_length=200)
    contact1 = PhoneNumberField.get_field()
    contact2 = PhoneNumberField.get_field()
    email = models.EmailField()
    language = models.CharField(max_length=max(map(lambda x: len(x[0]), LANGUAGES)),
                                choices=LANGUAGES,
                                default=ENGLISH)

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
    ACCOMPANIST = 'accompanist'
    PERFORMER = 'performer'
    ROLES = ((ACCOMPANIST, "Accompanist"), (PERFORMER, "Performer"))
    registration_entry = models.ForeignKey(
        ProsceniumTheatreRegistration, on_delete=models.CASCADE)
    role = models.CharField(max_length=max(map(lambda x: len(x[0]), ROLES)),
                            choices=ROLES,
                            default=PERFORMER)
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

    ENGLISH = 'en'
    HINDI = 'hi'
    KANNADA = 'ka'
    LANGUAGES = ((ENGLISH, "English"), (HINDI, "Hindi"), (KANNADA, "Kannada"))
    institution = models.CharField(max_length=200)
    contact1 = PhoneNumberField.get_field()
    contact2 = PhoneNumberField.get_field()
    email = models.EmailField()
    language = models.CharField(max_length=max(map(lambda x: len(x[0]), LANGUAGES)),
                                choices=LANGUAGES,
                                default=ENGLISH)

    def __str__(self):
        return f"Institution: {self.institution}, Language: {self.language}, 1st Contact No.: {self.contact1}, 2nd Contact No.: {self.contact2}, E-Mail ID: {self.email}"


class ProsceniumStreetPlayParticipant(models.Model):
    ACCOMPANIST = 'accompanist'    
    PERFORMER = 'performer'
    ROLES = ((ACCOMPANIST, "Accompanist"), (PERFORMER, "Performer"))
    registration_entry = models.ForeignKey(
        ProsceniumStreetPlayRegistration, on_delete=models.CASCADE)
    role = models.CharField(max_length=max(map(lambda x: len(x[0]), ROLES)),
                            choices=ROLES,
                            default=PERFORMER)
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
    BANGALORE = "BLR"
    KOLKATA = "CCU"
    CHENNAI = "MAD"
    DELHI = "DEL"
    MUMBAI = "BOM"
    PRELIMS_VENUES = ((BANGALORE, "Bangalore"), (KOLKATA, "Kolkata"),
                      (CHENNAI, "Chennai"), (DELHI, "Delhi"), (MUMBAI, "Mumbai"))

    band_name = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    email = models.EmailField()
    city = models.CharField(max_length=200)
    facebook_link = models.URLField()

    def upload_path(instance, filename):
        return f"./uploads/bob/audio/{instance.band_name} - {instance.city} - {filename}"

    audio_sample = models.FileField(
        validators=[AUDIO_FILE_VALIDATOR],
        max_length=255,
        upload_to=upload_path)

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
