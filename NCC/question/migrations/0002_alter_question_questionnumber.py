# Generated by Django 4.2.2 on 2023-10-18 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='questionNumber',
            field=models.IntegerField(unique=True),
        ),
    ]
