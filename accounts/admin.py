from django.contrib import admin
from .models import Contributor

class ContributorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'title', 'area_of_expertise', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'title', 'area_of_expertise')
    list_filter = ('created_at', 'updated_at', 'area_of_expertise')

admin.site.register(Contributor, ContributorAdmin)
