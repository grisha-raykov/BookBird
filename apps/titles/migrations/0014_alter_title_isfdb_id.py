# Generated by Django 5.1.4 on 2024-12-15 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0013_title_series_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='isfdb_id',
            field=models.IntegerField(blank=True, help_text='ISFDB ID for this title', null=True, unique=True),
        ),
    ]
