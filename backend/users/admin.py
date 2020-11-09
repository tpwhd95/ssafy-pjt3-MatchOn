from django.contrib import admin
from .models import User, BeforeMatch, AfterMatch


class BeforeMatchAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sports_name', 'user']
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
admin.site.register(User)
admin.site.register(BeforeMatch, BeforeMatchAdmin)
admin.site.register(AfterMatch)