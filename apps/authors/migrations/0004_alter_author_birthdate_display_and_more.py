# Generated by Django 5.1.4 on 2024-12-14 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0003_author_birthdate_display_author_deathdate_display_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='birthdate_display',
            field=models.CharField(blank=True, editable=False, help_text='Formatted birth date (YYYY-MM-DD or YYYY)', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='deathdate_display',
            field=models.CharField(blank=True, editable=False, help_text='Formatted death date (YYYY-MM-DD or YYYY)', max_length=10, null=True),
        ),
    ]