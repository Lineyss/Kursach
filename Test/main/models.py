from typing import Any
from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User
# Create your models here.

class Teg(models.Model):
    Title = models.CharField(max_length=100, verbose_name='Название')

class FileFolder(models.Model):
    IDTeg = models.ForeignKey(Teg, verbose_name='Тег', on_delete=models.CASCADE)

    def __str__(self):
        return super().__str__(self.pk)

class AFileFolder(models.Manager):

    IDUser = models.ManyToManyField(User, verbose_name='Пользователь')
    IDFileFolder = models.OneToOneField(FileFolder, on_delete=models.CASCADE, blank=True, editable=False, unique=True, verbose_name='Уникальный ID')
    Title = models.CharField(max_length=100, verbose_name='Название')
    Size = models.IntegerField(verbose_name='Размер')
    Date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', editable=False, blank=True)

    class Meta:
        abstract = True

    def create(self, *args, **kwargs):
        if self.IDFileFolder_id is None or self.IDFileFolder is None:
            fileFolder = FileFolder.objects.create()
            self.IDFileFolder = fileFolder
        return super().create(*args, **kwargs)
    
    def delete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]:
        FileFolder.objects.delete(pk = self.IDFileFolder)
        return super().delete(using, keep_parents)

class Folder(models.Model):
    IDFolder = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Папка где хранится папка', null=True, blank=True)

class File(models.Model):
    IDFolder = models.ForeignKey(Folder, on_delete=models.CASCADE, verbose_name='Папка где хранится файл')

class ActivityLog(models.Model):
    IDUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    IDFileFolder = models.ForeignKey(FileFolder, on_delete=models.CASCADE, verbose_name='Файл/папка')
    Action = models.CharField(max_length=100, verbose_name='Действие')
    Date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

class Premission(models.Model):
    Title = models.CharField(max_length=50 ,verbose_name='Название')

class SharedURI(models.Model):
    IDSender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель ссылки')
    IDPremission = models.ForeignKey(Premission, on_delete=models.CASCADE, verbose_name='Права')
    UrlAddress = models.CharField(max_length=50, verbose_name='Ссылка')
    DateCreate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', editable=False)
    DateDelete = models.DateTimeField(verbose_name='Дата деактивации', blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        self.DateDelete = self.DateCreate + timedelta(hours=1)
        super().save(*args, **kwargs)