from typing import Any
from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User
# Create your models here.

class Teg(models.Model):
    Title = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = 'Теги'

class FileFolder(models.Model):
    IDTeg = models.ForeignKey(Teg, verbose_name='Тег', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.pk}'
    
    class Meta:
        verbose_name = "Идентификатор файлов и папок"
        verbose_name_plural = 'Идентификатор файлов и папок'

class AFileFolder(models.Model):
    IDFileFolder = models.OneToOneField(FileFolder, on_delete=models.CASCADE, editable=False, unique=True, blank=True, null=True, verbose_name='Уникальный ID')
    Title = models.CharField(max_length=100, verbose_name='Название')
    Size = models.IntegerField(verbose_name='Размер')
    Date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', editable=False, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs)-> None:
        if self.IDFileFolder_id is None or self.IDFileFolder is None:
            fileFolder = FileFolder.objects.create()
            self.IDFileFolder = fileFolder

        return super().save(*args, **kwargs)
    
    def delete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]:
        FileFolder.objects.delete(pk = self.IDFileFolder)
        return super().delete(using, keep_parents)

class Folder(AFileFolder):
    IDUser = models.ManyToManyField(User, verbose_name='Пользователь(и)')
    IDFolder = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Папка где хранится папка', null=True, blank=True)

    class Meta:
        verbose_name = "Папка"
        verbose_name_plural = 'Папки'

class File(AFileFolder):
    IDUser = models.ManyToManyField(User, verbose_name='Пользователь(и)')
    IDFolder = models.ForeignKey('Folder', on_delete=models.CASCADE, verbose_name='Папка где хранится файл', null=True, blank=True)
    
    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = 'Файлы'

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
    UrlAddress = models.CharField(max_length=50, verbose_name='Ссылка')
    DateCreate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', editable=False)
    DateDelete = models.DateTimeField(verbose_name='Дата деактивации', blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        self.DateDelete = self.DateCreate + timedelta(hours=1)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ссылка доступа"
        verbose_name_plural = 'Ссылки доступа'