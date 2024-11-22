from django.urls import path
from .views import *

urlpatterns = [
    path('home', main, name='main'),
    path('file_folder/<int:id>/delete', delete_file_folder, name='delete'),
    path('file/create', file_create, name='file-create'),
    path('folder/create', folder_create, name='folder-create'),
    path('download/<int:id>', download, name='download')
]