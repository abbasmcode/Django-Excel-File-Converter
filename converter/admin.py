from django.contrib import admin
from .models import ConvertedFile

@admin.register(ConvertedFile)
class ConvertedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'excel_file', 'csv_file', 'json_file', 'zip_file', 'created_at')
