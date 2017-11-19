from django.contrib import admin
from .models import *


class ProsceniumTheatreParticipantInline(admin.TabularInline):
    model = ProsceniumTheatreParticipant
    extra = 0


class ProsceniumTheatreRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['institution', 'language', 'time', 'referral_code']}),
        ('Contact Information', {'fields': ['email', 'contact1', 'contact2']}),
        ('Prelims Information', {'fields': ['prelims_video', 'prelims_script']})
    ]
    inlines = [ProsceniumTheatreParticipantInline]


class ProsceniumStreetPlayParticipantInline(admin.TabularInline):
    model = ProsceniumStreetPlayParticipant
    extra = 0


class ProsceniumStreetPlayRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['institution', 'language', 'time', 'referral_code']}),
        ('Contact Information', {'fields': ['email', 'contact1', 'contact2']})
    ]
    inlines = [ProsceniumStreetPlayParticipantInline]


class BoBParticipantInline(admin.TabularInline):
    model = BoBParticipant
    extra = 0


class BoBRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['band_name', 'city', 'genre', 'time', 'referral_code']}),
        ('Contact Information', {'fields': ['email', 'facebook_link']}),
        ('Prelims Information', {'fields': ['prelims_venue', 'audio_sample_file', 'audio_sample_link']})
    ]
    inlines = [BoBParticipantInline]


class LasyaParticipantInline(admin.TabularInline):
    model = LasyaParticipant
    extra = 0


class LasyaRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'institution', 'time', 'referral_code']}),
        ('Contact Information', {'fields': ['email', 'contact']}),
        ('Prelims Information', {'fields': ['prelims_video', 'prelims_video_link']})
    ]
    inlines = [LasyaParticipantInline]


class SInECParticipantInline(admin.TabularInline):
    model = SInECParticipant
    extra = 0


class SInECRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['team_name', 'time', 'referral_code']}),
        ('Contact Information', {'fields': ['email', 'contact', 'address']}),
        ('Project Information', {'fields': ['project_name', 'project_field', 'registered_company', 'project_abstract', 'project_patented', 'project_file', 'privacy_preference']})
    ]
    inlines = [SInECParticipantInline]

admin.site.register(ProsceniumTheatreRegistration,
                    ProsceniumTheatreRegistrationAdmin)
admin.site.register(ProsceniumStreetPlayRegistration,
                    ProsceniumStreetPlayRegistrationAdmin)
admin.site.register(BoBRegistration,
                    BoBRegistrationAdmin)
admin.site.register(LasyaRegistration, LasyaRegistrationAdmin)
admin.site.register(SInECRegistration, SInECRegistrationAdmin)
