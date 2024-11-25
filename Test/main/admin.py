from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .forms import TegForm
from .models import *

# Register your models here.
@admin.register(Teg)
class TegAdmin(ImportExportModelAdmin):
    form = TegForm
    list_display = ('id', 'Title', 'Color', 'IDUser',)
    search_fields = ('Title', 'id', 'IDUser',)
    list_filter = ('Title', 'IDUser',)
    list_editable = ('Title', 'Color',)
    list_display_links = ('id', )

@admin.register(FileFolder)
class FileFolderAdmin(ImportExportModelAdmin):
    change_list_template = 'admin/user_summary.html'

    list_display = ('id', 'IDTeg', )

    def getDataForStats(self, model):
        return model.objects.count()

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['files'] = self.getDataForStats(File)
        extra_context['folders'] = self.getDataForStats(Folder)
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Folder)
class FolderAdmin(ImportExportModelAdmin):
    list_display = ('id', 'IDFileFolder', 'IDFolder', 'Title', 'Size', 'Date', 'Path',)
    list_display_links = ('id',)
    search_fields = ('id', 'Title', 'Size', 'Date', 'Path',)
    list_editable = ('Title', )
    list_filter = ('Owner', 'IDFolder', 'Date', 'Path',)
    fields = ('IDFolder', 'Owner', 'Title', 'AllowedUsers', )

@admin.register(File)
class FileAdmin(ImportExportModelAdmin):
    list_display = ('id', 'IDFileFolder', 'IDFolder', 'Title', 'Size', 'Date', 'Path',)
    list_display_links = ('id',)
    search_fields = ('id', 'Title', 'Size', 'Date', 'Path',)
    list_editable = ('Title', )
    list_filter = ('Owner', 'IDFolder', 'Date', 'Path',)
    fields = ('IDFolder', 'File', 'Owner', 'AllowedUsers', )

    def save_model(self, request, obj, form, change):
        return super().save_model(request, obj, form, change)

@admin.register(ActivityLog)
class ActivityLogAdmin(ImportExportModelAdmin):
    list_display = ('id', 'IDUser', 'IDFileFolder', 'Action', 'Date', )
    list_display_links = ('id',)
    search_fields = ('id', 'Action', )
    list_editable = ('Action', )
    list_filter = ('IDUser', 'IDFileFolder', 'Date', )

@admin.register(SharedURI)
class SharedURIAdmin(ImportExportModelAdmin):
    list_display = ('id', 'IDSender', 'Premissions', 'Token', 'DateCreate', 'DateDelete')
    list_display_links = ('id',)
    search_fields = ('id', 'Token', )
    list_filter = ('DateCreate', 'DateDelete', 'IDSender', 'Premissions', )
    fields = ('IDSender', 'Premissions', 'IDFileFolder', )