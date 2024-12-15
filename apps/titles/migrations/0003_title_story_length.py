# Generated by Django 5.1.4 on 2024-12-15 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0002_alter_title_options_title_content_indicator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='story_length',
            field=models.CharField(blank=True, choices=[('NOVELLA', 'Novella'), ('NOVELETTE', 'Novelette'), ('SHORTSTORY', 'Short Story')], help_text='Length category for short fiction titles', max_length=20, null=True),
        ),
    ]
