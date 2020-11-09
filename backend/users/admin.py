from django.contrib import admin
from .models import User, BeforeMatch, AfterMatch


class BeforeMatchAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sports_name', 'status', 'user']
    list_filter = ('sports_name', 'status')


class AfterMatchAdmin(admin.ModelAdmin):
    list_display = ['pk', 'before_match', 'matching_pk']
    list_filter = ['matching_pk']

admin.site.register(User)
admin.site.register(BeforeMatch, BeforeMatchAdmin)
admin.site.register(AfterMatch, AfterMatchAdmin)