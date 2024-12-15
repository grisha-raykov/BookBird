# Generated by Django 5.1.4 on 2024-12-15 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0003_title_story_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='TitleTransliteration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transliterated_text', models.TextField(help_text='Romanized version of the title', verbose_name='Romanized Text')),
                ('notes', models.TextField(blank=True, help_text='Additional notes about this transliteration', null=True, verbose_name='Notes')),
                ('title', models.ForeignKey(help_text='The original title this transliteration belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='transliterations', to='titles.title', verbose_name='Title')),
            ],
            options={
                'verbose_name': 'Title Transliteration',
                'verbose_name_plural': 'Title Transliterations',
                'ordering': ['transliterated_text'],
            },
        ),
    ]