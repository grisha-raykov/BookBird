# Generated by Django 5.1.4 on 2024-12-15 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0004_titletransliteration'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='isfdb_id',
            field=models.IntegerField(blank=True, help_text='ISFDB ID for this title', null=True),
        ),
    ]