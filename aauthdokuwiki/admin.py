from django.contrib import admin
from .models import DokuwikiUser


class DokuwikiUserAdmin(admin.ModelAdmin):
        list_display = ('user',)
        search_fields = ('user__username',)

admin.site.register(DokuwikiUser, DokuwikiUserAdmin)
