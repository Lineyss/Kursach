from django.urls import path
from .views import *

urlpatterns = [
    path('home/', main, name='main'),
    path('home/<path:path>', main),

    path('file_folder/<int:id>/delete', delete_file_folder, name='delete'),
    path('file/create', file_create, name='file-create'),
    path('folder/create', folder_create, name='folder-create'),
    path('update/<int:id>/<str:title>', update_file_folder_name, name='update-name'),
    path('move/<int:idMoveFileFolder>/<int:idToMoveFolder>', move_file_folder),

    path('teg/update/<int:id>', update_teg, name='update_teg'),
    path('teg/delete/<int:id>', delete_teg, name='delete_teg'),
    path('teg/add/<int:teg_id>/<int:file_folder_id>', add_teg_to_file_folder, name='add_teg'),

    path('download/<int:id>', download_req, name='download_id'),
    path('download/<str:token>', download_token, name='download_token'),
    path('download/add/<int:id>', create_download_links, name='create_download_link'),
    path('delete/download',delete_download_links, name='delete_download_link')
]