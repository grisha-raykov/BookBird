# Generated by Django 5.1.4 on 2024-12-14 12:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0003_alter_language_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='native_name',
            field=models.CharField(blank=True, help_text="Language name in its native form (e.g. 'English', 'Български')", max_length=255, null=True, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
    ]