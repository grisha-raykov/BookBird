# Generated by Django 5.1.4 on 2024-12-15 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0002_authortransliteration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authortransliteration',
            name='notes',
        ),
    ]