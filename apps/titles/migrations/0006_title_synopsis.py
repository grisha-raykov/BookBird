# Generated by Django 5.1.4 on 2024-12-15 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0005_title_isfdb_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='synopsis',
            field=models.TextField(blank=True, help_text='Synopsis of the work', null=True),
        ),
    ]
