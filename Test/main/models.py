from guardian.shortcuts import assign_perm, get_objects_for_user
from django.core.management.utils import get_random_secret_key
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from datetime import timedelta
from django.db import models
from typing import Any
import datetime as dt
import os

class Teg(models.Model):
    Title = models.CharField(max_length=10, verbose_name='Название')
    Color = models.CharField(max_length=7, default='#FFFFFF', verbose_name='Цвет')
    IDUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Принадлежит')
    DateTime = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', editable=False, blank=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.Title.__str__() 

class FileFolder(models.Model):
    IDTeg = models.ForeignKey(Teg, verbose_name='Тег', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.get_file_or_folder().Path}'
    
    class Meta:
        verbose_name = "Идентификатор файлов и папок"
        verbose_name_plural = 'Идентификатор файлов и папок'

    def get_related_folder(self):
        try:
            return self.folder
        except Folder.DoesNotExist:
            return None

    def get_related_file(self):
        try:
            return self.file
        except File.DoesNotExist:
            return None
        
    def get_file_or_folder(self):
        obj = self.get_related_file()
        if obj is None:
            obj = self.get_related_folder()

        return obj

class AFileFolder(models.Model):
    Path = models.CharField(default='/', verbose_name='Путь', max_length=100, blank=True, null=True)
    Title = models.CharField(verbose_name='Название', max_length=100)
    IDFileFolder = models.OneToOneField(FileFolder, on_delete=models.CASCADE, editable=False, unique=True, blank=True, null=True, verbose_name='Уникальный ID')
    Size = models.IntegerField(verbose_name='Размер', default=0, blank=True)
    Date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', editable=False, blank=True)
    AllowedUsers = models.ManyToManyField(User, verbose_name='Доступна пользователяи:', blank=True, null=True)

    class Meta:
        abstract = True
        permissions = [
            ("delete", "Can delete own object"),
            ("update", "Can change name own object"),
            ("open", "Can open own object"),
            ("download", "Can download open own object")
        ]

    def change_title(self, count):
        if '.' in self.Title:
            split_filename = self.Title.rsplit(".")
            split_filename[0] += f" ({count})"
            self.Title = ".".join(split_filename)
        else:
            self.Title += f" ({count})"

    def check_unique_title(self):
        count = 1
        if self.is_file:
            while File.objects.filter(IDFolder=self.IDFolder, Title=self.Title).exclude(id=self.id).exists() or Folder.objects.filter(IDFolder=self.IDFolder, Title=self.Title):
                self.change_title(count)
                count += 1
        else:
            while File.objects.filter(IDFolder=self.IDFolder, Title=self.Title).exists() or Folder.objects.filter(IDFolder=self.IDFolder, Title=self.Title).exclude(id=self.id):
                self.change_title(count)
                count+=1

    def __str__(self):
        return f'{self.Path}{self.Title}'

    def save(self, *args, **kwargs)-> None:
        if self.IDFileFolder_id is None or self.IDFileFolder is None:
            fileFolder = FileFolder.objects.create()
            self.IDFileFolder = fileFolder

        return super().save(*args, **kwargs)
    
    def delete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]:
        FileFolder.objects.filter(id=self.IDFileFolder.id).first().delete()
        return super().delete(using, keep_parents)

class Folder(AFileFolder):
    IDFolder = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Папка где хранится папка', null=True, blank=True)
    Owner = models.ForeignKey(User, verbose_name='Владелец)', on_delete=models.CASCADE, related_name='folder_folder')

    is_file = False

    class Meta:
        verbose_name = "Папка"
        verbose_name_plural = 'Папки'

    def save(self, *args, **kwargs):
        
        
        self.check_unique_title()
        
        if self.IDFolder is not None:
            self.Size += self.IDFolder.Size
            self.Path = f'{self.IDFolder.Path}/{self.Title}'
        else:
            self.Size = sum(file.Size for file in File.objects.filter(IDFolder_id = self.pk))
            self.Path = f'/{self.Title}'


        save = super().save(*args, **kwargs)

        permissions = Permission.objects.filter(content_type__model='Folder')
        for perm in permissions:
            assign_perm(perm.name, self.Owner, self)

        return save

class File(AFileFolder):
    IDFolder = models.ForeignKey('Folder', on_delete=models.CASCADE, verbose_name='Папка где хранится файл', null=True, blank=True, related_name='files')
    File = models.FileField(verbose_name='Файл')
    Owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE, related_name='file_folder')
    
    is_file = True
    
    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = 'Файлы'

    def rename_file(self):
        current_file_name = self.File.name

        new_file_name = os.path.join(os.path.dirname(current_file_name), self.Title)
        new_file_path = os.path.join(os.path.dirname(self.File.path), self.Title)


        if os.path.exists(self.File.path):
            os.rename(self.File.path, new_file_path)

        self.File.name = new_file_name


    def set_values(self):
        file_title = os.path.basename(self.File.name)

        if self.Title == '':
            self.Title = file_title
            self.Path = f'/{self.Title}'
        
        self.check_unique_title()

        if self.Title != file_title:
            self.Path = f'/{self.Title}'

        if self.IDFolder is not None:
            self.Path = f'/{self.IDFolder.Title}/{self.Title}'
            self.IDFolder.Size += self.Size

    def save(self, *args, **kwargs):
        self.Size = self.File.size
        self.set_values()

        save = super().save(*args, **kwargs)
        
        permissions = Permission.objects.filter(content_type__model='File')
        for perm in permissions:
            assign_perm(perm.name, self.Owner, self)

        return save


    def delete(self, *args, **kwargs):
        path = os.path.dirname(self.File.name)
        os.remove(path)
        if self.IDFolder is not None:
            self.IDFileFolder.Size -= self.Size

        return super().delete(*args, **kwargs)

class ActivityLog(models.Model):
    IDUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    IDFileFolder = models.ForeignKey(FileFolder, on_delete=models.CASCADE, verbose_name='Файл/папка')
    Action = models.CharField(max_length=100, verbose_name='Действие')
    Date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = "Логи"
        verbose_name_plural = 'Логи'

class SharedURI(models.Model):
    IDSender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель ссылки')
    Premissions = models.CharField(max_length=100)
    IDFileFolder = models.ForeignKey(FileFolder, on_delete=models.CASCADE, verbose_name='Папка/Файл')
    Token = models.CharField(max_length=50, verbose_name='Токен', editable=False, blank=True, default=get_random_secret_key())
    DateCreate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, editable=False)
    DateDelete = models.DateTimeField(verbose_name='Дата деактивации', blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.DateDelete = timedelta(hours=1) + dt.datetime.now()
        
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ссылка доступа"
        verbose_name_plural = 'Ссылки доступа'