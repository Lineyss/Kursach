from django.urls import path
from .views import *

urlpatterns = [
    path('home/', main, name='main'),
    path('home/<path:path>', main),

    path('file_folder/<int:id>/delete', delete_file_folder, name='delete'),
    path('file/create', file_create, name='file-create'),
    path('folder/create', folder_create, name='folder-create'),
    path('update/<int:id>/<str:title>', update_file_folder_name, name='update-name'),
    path('download/<int:id>', download, name='download'),
    path('move/<int:idMoveFileFolder>/<int:idToMoveFolder>', move_file_folder),

    path('teg/update/<int:id>', update_teg, name='update_teg'),
    path('teg/delete/<int:id>', delete_teg, name='delete_teg'),
    path('teg/add/<int:teg_id>/<int:file_folder_id>', add_teg_to_file_folder, name='add_teg')
]