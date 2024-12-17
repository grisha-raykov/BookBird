# Generated by Django 5.1.4 on 2024-12-16 18:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0006_publication_ctype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='pages',
            field=models.CharField(blank=True, help_text='Number of pages', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publisher',
            field=models.ForeignKey(blank=True, help_text='Publisher of this publication', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='publications', to='publications.publisher'),
        ),
    ]