from django.contrib.auth.models import User
from datetime import timedelta
from django.db import models
from typing import Any
import os

# Create your models here.

class Teg(models.Model):
    Title = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = 'Теги'

class FileFolder(models.Model):
    IDTeg = models.ForeignKey(Teg, verbose_name='Тег', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.pk}'
    
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


class AFileFolder(models.Model):
    Path = models.CharField(default='/', verbose_name='Путь', max_length=100, blank=True, null=True)
    Title = models.CharField(verbose_name='Название', max_length=100)
    IDFileFolder = models.OneToOneField(FileFolder, on_delete=models.CASCADE, editable=False, unique=True, blank=True, null=True, verbose_name='Уникальный ID')
    Size = models.IntegerField(verbose_name='Размер', default=0, blank=True)
    Date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', editable=False, blank=True)

    class Meta:
        abstract = True

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
    IDUser = models.ManyToManyField(User, verbose_name='Пользователь(и)')
    IDFolder = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Папка где хранится папка', null=True, blank=True)

    is_file = False

    class Meta:
        verbose_name = "Папка"
        verbose_name_plural = 'Папки'

    def save(self, *args, **kwargs):
        if self.IDFolder is not None:
            self.Size += self.IDFolder.Size
            self.Path += self.IDFolder.Path
        else:
            self.Size = sum(file.Size for file in File.objects.filter(IDFolder_id = self.pk))
            self.Path = '/'

        return super().save(*args, **kwargs)


def user_directory_path(instance, filename):
    return f"uploads/{filename}"

class File(AFileFolder):
    IDUser = models.ManyToManyField(User, verbose_name='Пользователь(и)')
    IDFolder = models.ForeignKey('Folder', on_delete=models.CASCADE, verbose_name='Папка где хранится файл', null=True, blank=True)
    File = models.FileField(upload_to=user_directory_path, verbose_name='Файл')
    
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
        else:
            os.remove(self.File.path)
            file = open(new_file_path, 'x')
            file.close()

        self.File.name = new_file_name

    def check_unique_title(self):
        while (self.IDFolder is not None and self.IDFolder.get_files()) or File.objects.filter(IDUser=self.IDUser, IDFolder=None, Title=self.Title).exists():
            split_filename = self.Title.split(".")
            split_filename[0] += " (1)"
            self.Title = ".".join(split_filename)

    def set_values(self):
        file_title = os.path.basename(self.File.name)

        if self.Title == '':
            self.Title = file_title
            self.Path = f'/{self.Title}'
        
        self.check_unique_title()

        if self.Title != file_title:
            self.rename_file()
            self.Path = f'/{self.Title}'

        if self.IDFolder is not None:
            self.Path = f'/{self.IDFolder.Title}/{self.Title}'
            self.IDFolder.Size += self.Size

    def save(self, *args, **kwargs):
        self.Size = self.File.size

        self.set_values()
        return super().save(*args, **kwargs) 


    def delete(self, *args, **kwargs):
        path = os.path.dirname(self.File.name)
        print(path)
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

class Premission(models.Model):
    Title = models.CharField(max_length=50 ,verbose_name='Название')

    class Meta:
        verbose_name = "Права доступа"
        verbose_name_plural = 'Права доступа'

class SharedURI(models.Model):
    IDSender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель ссылки')
    IDPremission = models.ForeignKey(Premission, on_delete=models.CASCADE, verbose_name='Права')
    IDFileFolder = models.ForeignKey(FileFolder, on_delete=models.CASCADE, verbose_name='Папка/Файл')
    UrlAddress = models.CharField(max_length=50, verbose_name='Ссылка')
    DateCreate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', editable=False)
    DateDelete = models.DateTimeField(verbose_name='Дата деактивации', blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        self.DateDelete = self.DateCreate + timedelta(hours=1)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ссылка доступа"
        verbose_name_plural = 'Ссылки доступа'