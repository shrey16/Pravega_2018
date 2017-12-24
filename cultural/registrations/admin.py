from django.contrib import admin
from .models import *


class ProsceniumTheatreParticipantInline(admin.TabularInline):
    model = ProsceniumTheatreParticipant
    readonly_fields = ('photo_preview',)
    extra = 0


class ProsceniumTheatreRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['institution',
                           'language', 'time', 'referral_code']}),
        ('Contact Information', {'fields': ['email', 'contact1', 'contact2']}),
        ('Prelims Information', {'fields': [
         'prelims_video', 'prelims_script']})
    ]
    inlines = [ProsceniumTheatreParticipantInline]


class ProsceniumStreetPlayParticipantInline(admin.TabularInline):
    model = ProsceniumStreetPlayParticipant
    readonly_fields = ('photo_preview',)
    extra = 0


class ProsceniumStreetPlayRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['institution',
                           'language', 'time', 'referral_code']}),
        ('Contact Information', {'fields': ['email', 'contact1', 'contact2']})
    ]
    inlines = [ProsceniumStreetPlayParticipantInline]


class BoBParticipantInline(admin.TabularInline):
    model = BoBParticipant
    extra = 0


class BoBRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['band_name', 'city',
                           'genre', 'time', 'referral_code']}),
        ('Contact Information', {'fields': ['email', 'facebook_link']}),
        ('Prelims Information', {'fields': [
         'prelims_venue', 'audio_sample_file', 'audio_sample_link']})
    ]
    inlines = [BoBParticipantInline]


class LasyaParticipantInline(admin.TabularInline):
    model = LasyaParticipant
    extra = 0


class LasyaRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'institution', 'time', 'referral_code']}),
        ('Contact Information', {'fields': ['email', 'contact']}),
        ('Prelims Information', {'fields': [
         'prelims_video', 'prelims_video_link']})
    ]
    inlines = [LasyaParticipantInline]


class SInECParticipantInline(admin.TabularInline):
    model = SInECParticipant
    extra = 0


class SInECRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['team_name', 'time', 'referral_code']}),
        ('Contact Information', {'fields': ['email', 'contact', 'address']}),
        ('Project Information', {'fields': ['project_name', 'project_field', 'registered_company',
                                            'project_abstract', 'project_patented', 'project_file', 'project_video', 'privacy_preference']})
    ]
    inlines = [SInECParticipantInline]


class DecoherenceParticipantInline(admin.TabularInline):
    model = DecoherenceParticipant
    extra = 0


class DecoherenceRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['team_name', 'time', 'referral_code']})
    ]
    inlines = [DecoherenceParticipantInline]

class OpenMicParticipantInline(admin.TabularInline):
    model = OpenMicParticipant
    extra = 0


class OpenMicRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'time', 'referral_code']}),
        ('Contact Information', {'fields': ['email']}),
        ('Additional Information', {'fields': [
         'expected_performance_duration_mins', 'instrument_requirement', 'reason_for_gt_3_members']})
    ]
    inlines = [OpenMicParticipantInline]

    def get_inline_instances(self, request, obj=None):
        unfiltered = super(OpenMicRegistrationAdmin,
                           self).get_inline_instances(request, obj)
        if obj and isinstance(obj, OpenMicRegistration):
            if len(obj.openmicparticipant_set.all()) <= 3:
                self.fieldsets[2][1]['fields'] = self.fieldsets[2][1][
                    'fields'][:-1]
        return unfiltered


class HackathonParticipantInline(admin.TabularInline):
    model = HackathonParticipant
    extra = 0


class HackathonRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['team_name', 'time', 'referral_code']}),
        ('Contact Information', {'fields': ['email', 'contact']}),
        ('Abstract', {'fields': ['abstract']}),
    ]
    inlines = [HackathonParticipantInline]

admin.site.register(ProsceniumTheatreRegistration,
                    ProsceniumTheatreRegistrationAdmin)
admin.site.register(ProsceniumStreetPlayRegistration,
                    ProsceniumStreetPlayRegistrationAdmin)
admin.site.register(BoBRegistration,
                    BoBRegistrationAdmin)
admin.site.register(LasyaRegistration, LasyaRegistrationAdmin)
admin.site.register(SInECRegistration, SInECRegistrationAdmin)
admin.site.register(OpenMicRegistration, OpenMicRegistrationAdmin)
admin.site.register(DecoherenceRegistration, DecoherenceRegistrationAdmin)
admin.site.register(HackathonRegistration, HackathonRegistrationAdmin)
