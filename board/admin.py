from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin

# Register your models here.
from .models import CodeOption

class CodeOptionAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

admin.site.register(CodeOption, CodeOptionAdmin)
