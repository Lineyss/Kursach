from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Teg)
class TegAdmin(ImportExportModelAdmin):
    pass

@admin.register(FileFolder)
class FileFolderAdmin(ImportExportModelAdmin):
    pass

@admin.register(Folder)
class FolderAdmin(ImportExportModelAdmin):
    pass

@admin.register(File)
class FileAdmin(ImportExportModelAdmin):
    pass

@admin.register(ActivityLog)
class ActivityLog(ImportExportModelAdmin):
    pass

@admin.register(Premission)
class Premission(ImportExportModelAdmin):
    pass

@admin.register(SharedURI)
class SharedURI(ImportExportModelAdmin):
    pass