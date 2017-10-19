from django.contrib import admin
from .models import *


class ProsceniumTheatreParticipantInline(admin.TabularInline):
    model = ProsceniumTheatreParticipant
    extra = 0


class ProsceniumTheatreRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['institution', 'language']}),
        ('Contact Information', {'fields': ['email', 'contact1', 'contact2']})
    ]
    inlines = [ProsceniumTheatreParticipantInline]


class ProsceniumStreetPlayParticipantInline(admin.TabularInline):
    model = ProsceniumStreetPlayParticipant
    extra = 0


class ProsceniumStreetPlayRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['institution', 'language']}),
        ('Contact Information', {'fields': ['email', 'contact1', 'contact2']})
    ]
    inlines = [ProsceniumStreetPlayParticipantInline]


class BoBParticipantInline(admin.TabularInline):
    model = BoBParticipant
    extra = 0


class BoBRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['band_name', 'city', 'genre', 'prelims_venue']}),
        ('Contact Information', {'fields': ['email', 'facebook_link']})
    ]
    inlines = [BoBParticipantInline]


admin.site.register(ProsceniumTheatreRegistration,
                    ProsceniumTheatreRegistrationAdmin)
admin.site.register(ProsceniumStreetPlayRegistration,
                    ProsceniumStreetPlayRegistrationAdmin)
admin.site.register(BoBRegistration,
                    BoBRegistrationAdmin)
