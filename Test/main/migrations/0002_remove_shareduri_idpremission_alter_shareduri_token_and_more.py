# Generated by Django 5.1.2 on 2024-11-25 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shareduri',
            name='IDPremission',
        ),
        migrations.AlterField(
            model_name='shareduri',
            name='Token',
            field=models.CharField(blank=True, default='1$t*g+5mbefu$=_lt(4v0mm)%=u5e8*vd16^5^fo8&551w1=15', editable=False, max_length=50, verbose_name='Токен'),
        ),
        migrations.DeleteModel(
            name='Premission',
        ),
    ]
