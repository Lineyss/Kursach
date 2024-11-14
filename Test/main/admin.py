from django.http import HttpRequest
from django.template.response import TemplateResponse
from import_export.admin import ImportExportModelAdmin
from django.db.models import Count
from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Teg)
class TegAdmin(ImportExportModelAdmin):
    list_display = ('id', 'Title', )
    list_display_links = ('id', )
    search_fields = ('Title', 'id', )
    list_editable = ('Title', )

@admin.register(FileFolder)
class FileFolderAdmin(ImportExportModelAdmin):
    change_list_template = 'admin/user_summary.html'

    def getDataForStats(self, model):
        return model.objects.count()

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['files'] = self.getDataForStats(File)
        extra_context['folders'] = self.getDataForStats(Folder)
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Folder)
class FolderAdmin(ImportExportModelAdmin):
    list_display = ('id', 'IDFileFolder', 'IDFolder', 'Title', 'Size', 'Date', )
    list_display_links = ('id',)
    search_fields = ('id', 'Title', 'Size', 'Date', )
    list_editable = ('Title', )
    list_filter = ('IDUser', 'IDFolder', 'Date', )
    fields = ('IDFolder', 'IDUser', 'Title')
    

@admin.register(File)
class FileAdmin(ImportExportModelAdmin):
    list_display = ('id', 'IDFileFolder', 'IDFolder', 'Title', 'Size', 'Date', )
    list_display_links = ('id',)
    search_fields = ('id', 'Title', 'Size', 'Date', )
    list_editable = ('Title', )
    list_filter = ('IDUser', 'IDFolder', 'Date', )
    fields = ('IDFolder', 'IDUser', 'File')

@admin.register(ActivityLog)
class ActivityLogAdmin(ImportExportModelAdmin):
    list_display = ('id', 'IDUser', 'IDFileFolder', 'Action', 'Date', )
    list_display_links = ('id',)
    search_fields = ('id', 'Action', )
    list_editable = ('Action', )
    list_filter = ('IDUser', 'IDFileFolder', 'Date', )

@admin.register(Premission)
class PremissionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'Title', )
    list_display_links = ('id',)
    search_fields = ('id', 'Title', )
    list_editable = ('Title', )

@admin.register(SharedURI)
class SharedURIAdmin(ImportExportModelAdmin):
    list_display = ('id', 'IDSender', 'IDPremission', 'UrlAddress', 'DateCreate', 'DateDelete')
    list_display_links = ('id',)
    search_fields = ('id', 'UrlAddress', )
    list_filter = ('DateCreate', 'DateDelete', 'IDSender', 'IDPremission')