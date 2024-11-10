# Generated by Django 5.1.2 on 2024-11-08 10:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileFolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Идентификатор файлов и папок',
                'verbose_name_plural': 'Идентификатор файлов и папок',
            },
        ),
        migrations.CreateModel(
            name='Premission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=50, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Права доступа',
                'verbose_name_plural': 'Права доступа',
            },
        ),
        migrations.CreateModel(
            name='Teg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Action', models.CharField(max_length=100, verbose_name='Действие')),
                ('Date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('IDUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('IDFileFolder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.filefolder', verbose_name='Файл/папка')),
            ],
            options={
                'verbose_name': 'Логи',
                'verbose_name_plural': 'Логи',
            },
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=100, verbose_name='Название')),
                ('Size', models.IntegerField(verbose_name='Размер')),
                ('Date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('IDFileFolder', models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.filefolder', verbose_name='Уникальный ID')),
                ('IDFolder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.folder', verbose_name='Папка где хранится папка')),
                ('IDUser', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Пользователь(и)')),
            ],
            options={
                'verbose_name': 'Папка',
                'verbose_name_plural': 'Папки',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=100, verbose_name='Название')),
                ('Size', models.IntegerField(verbose_name='Размер')),
                ('Date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('IDUser', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Пользователь(и)')),
                ('IDFileFolder', models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.filefolder', verbose_name='Уникальный ID')),
                ('IDFolder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.folder', verbose_name='Папка где хранится файл')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
        migrations.CreateModel(
            name='SharedURI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UrlAddress', models.CharField(max_length=50, verbose_name='Ссылка')),
                ('DateCreate', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('DateDelete', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Дата деактивации')),
                ('IDPremission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.premission', verbose_name='Права')),
                ('IDSender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Создатель ссылки')),
            ],
            options={
                'verbose_name': 'Ссылка доступа',
                'verbose_name_plural': 'Ссылки доступа',
            },
        ),
        migrations.AddField(
            model_name='filefolder',
            name='IDTeg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.teg', verbose_name='Тег'),
        ),
    ]
