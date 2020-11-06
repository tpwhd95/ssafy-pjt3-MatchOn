from django.contrib import admin
from .models import Sports, Match, MatchUser, Locations

class MatchAdmin(admin.ModelAdmin):
    list_display = ['sports', 'pk']

# class UserAdmin(admin.ModelAdmin):
#     list_display = ['nickname']
# class BeforeMatchAdmin(admin.ModelAdmin):
#     search_fields = ['title']
#     list_display = '__all__'

# class WeatherLikeAdmin(admin.ModelAdmin):
#     list_display = ['movie', 'weather', 'user', ]

# class RankAdmin(admin.ModelAdmin):
#     list_display = ['movie']

# admin.site.register(Genre, GenreAdmin)
admin.site.register(Sports)
admin.site.register(Match, MatchAdmin)
admin.site.register(MatchUser)
admin.site.register(Locations)