import sys
import json
from .models import *


class RegistrationData:

    def load_from_db(self):
        pass

    def dump_to_json(self):
        raw_data = list(map(lambda x: {'serial_no': x[0], 'entry': x[
                        1].__dict__}, enumerate(self.load_from_db())))
        data = {}
        data['total_entries'] = len(raw_data)
        data['entries'] = raw_data
        return json.dumps(data, indent=4)

    def save_all_data_as_json(self, file=sys.stdout):
        print(self.dump_to_json(), file=file)


class ProsceniumTheatreRegistrationData(RegistrationData):

    def load_from_db(self):
        for registration in ProsceniumTheatreRegistration.objects.all():
            data = ProsceniumTheatreRegistrationData()
            data.institution = registration.institution
            data.language = registration.language
            data.contact1 = registration.contact1
            data.contact2 = registration.contact2
            data.email = registration.email
            data.prelims_video = str(registration.prelims_video)
            data.prelims_script = str(registration.prelims_script)
            data.participants = []
            data.accompanists = []
            for participant in registration.prosceniumtheatreparticipant_set.all():
                participant_data = {}
                participant_data['name'] = participant.name
                participant_data['age'] = participant.age
                if participant.role == ProsceniumTheatreParticipant.PARTICIPANT:
                    data.participants.append(participant_data)
                elif participant.role == ProsceniumTheatreParticipant.ACCOMPANIST:
                    data.accompanists.append(participant_data)
            data.participant_count = len(data.participants)
            data.accompanist_count = len(data.accompanists)
            yield data


class ProsceniumStreetPlayRegistrationData(RegistrationData):

    def load_from_db(self):
        for registration in ProsceniumStreetPlayRegistration.objects.all():
            data = ProsceniumTheatreRegistrationData()
            data.institution = registration.institution
            data.language = registration.language
            data.contact1 = registration.contact1
            data.contact2 = registration.contact2
            data.email = registration.email
            data.participants = []
            data.accompanists = []
            for participant in registration.prosceniumstreetplayparticipant_set.all():
                participant_data = {}
                participant_data['name'] = participant.name
                participant_data['age'] = participant.age
                participant_data['photo'] = str(participant.photo)
                if participant.role == ProsceniumTheatreParticipant.PARTICIPANT:
                    data.participants.append(participant_data)
                elif participant.role == ProsceniumTheatreParticipant.ACCOMPANIST:
                    data.accompanists.append(participant_data)
            data.participant_count = len(data.participants)
            data.accompanist_count = len(data.accompanists)
            yield data


class BoBRegistrationData(RegistrationData):

    def load_from_db(self):
        for registration in BoBRegistration.objects.all():
            data = ProsceniumTheatreRegistrationData()
            data.band_name = registration.band_name
            data.city = registration.city
            data.genre = registration.genre
            data.facebook = registration.facebook_link
            data.email = registration.email
            data.prelims_venue = registration.prelims_venue
            data.audio_sample = str(registration.audio_sample)
            data.participants = []
            for participant in registration.bobparticipant_set.all():
                participant_data = {}
                participant_data['name'] = participant.name
                participant_data['contact'] = participant.contact
                participant_data['instrument'] = participant.instrument
                data.participants.append(participant_data)
            data.participant_count = len(data.participants)
            yield data
