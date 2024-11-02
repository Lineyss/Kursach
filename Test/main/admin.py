from import_export.admin import ImportExportModelAdmin
from django.shortcuts import render
from django.db.models import Count
from django.contrib import admin
from django.urls import path
from .models import *

# Register your models here.

@admin.register(Teg)
class TegAdmin(ImportExportModelAdmin):
    pass

@admin.register(FileFolder)
class FileFolderAdmin(ImportExportModelAdmin):
    change_list_template = 'admin/user_summary.html'
    def getDataForStats(self, model):
        return File.objects.count()

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['files'] = self.getDataForStats(File)
        extra_context['folders'] = self.getDataForStats(Folder)
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Folder)
class FolderAdmin(ImportExportModelAdmin):
    pass

@admin.register(File)
class FileAdmin(ImportExportModelAdmin):
    pass

@admin.register(ActivityLog)
class ActivityLogAdmin(ImportExportModelAdmin):
    pass

@admin.register(Premission)
class PremissionAdmin(ImportExportModelAdmin):
    pass

@admin.register(SharedURI)
class SharedURIAdmin(ImportExportModelAdmin):
    pass