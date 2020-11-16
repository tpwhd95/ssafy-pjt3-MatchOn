from django.contrib import admin
from .models import Sports, Match, MatchUser, Locations

class MatchAdmin(admin.ModelAdmin):
    list_display = ['sports', 'pk']


class MatchUserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'match', 'user_pk', 'team']
    list_filter = ['match']


# class UserAdmin(admin.ModelAdmin):
#     list_display = ['nickname']


# class WeatherLikeAdmin(admin.ModelAdmin):
#     list_display = ['movie', 'weather', 'user', ]

# class RankAdmin(admin.ModelAdmin):
#     list_display = ['movie']

# admin.site.register(Genre, GenreAdmin)
admin.site.register(Sports)
admin.site.register(Match, MatchAdmin)
admin.site.register(MatchUser, MatchUserAdmin)
admin.site.register(Locations)