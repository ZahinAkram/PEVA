from django.contrib import admin

from .models import Event, Shared_Event

admin.site.register(Event),
admin.site.register(Shared_Event)