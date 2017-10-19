from django.contrib import admin
from .models import ProsceniumParticipant, ProsceniumRegistration


class ProsceniumParticipantInline(admin.TabularInline):
    model = ProsceniumParticipant
    extra = 3


class ProsceniumRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['institution']}),
        ('Contact Information', {'fields': ['email', 'contact1', 'contact2']})
    ]
    inlines = [ProsceniumParticipantInline]

admin.site.register(ProsceniumRegistration, ProsceniumRegistrationAdmin)
