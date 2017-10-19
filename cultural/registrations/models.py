from django.db import models
from .customfields import IntegerRangeField, PhoneNumberField


class ProsceniumRegistration(models.Model):
    institution = models.CharField(max_length=200)
    contact1 = PhoneNumberField.get_field()
    contact2 = PhoneNumberField.get_field()
    email = models.EmailField()

    def __str__(self):
        return f"Institution: {self.institution}, 1st Contact No.: {self.contact1}, 2nd Contact No.: {self.contact2}, E-Mail ID: {self.email}"


class ProsceniumParticipant(models.Model):
    ACCOMPANIST = "accompanist"
    PARTICIPANT = "participant"
    ROLES = ((ACCOMPANIST, "Accompanist"), (PARTICIPANT, "Participant"))
    registration_entry = models.ForeignKey(ProsceniumRegistration, on_delete=models.CASCADE)
    role = models.CharField(max_length=max(map(lambda x: len(x[0]), ROLES)),
                            choices=ROLES,
                            default=PARTICIPANT)
    age = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"Registration Entry: {self.registration_entry}, Name: {self.name}, Age: {self.age}, Role: {self.role}"
