# Generated by Django 5.0.2 on 2024-04-01 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cramschool_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]