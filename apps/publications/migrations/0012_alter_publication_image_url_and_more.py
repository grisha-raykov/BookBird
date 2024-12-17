# Generated by Django 5.1.4 on 2024-12-17 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0011_publicationauthor_publication_authors_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='image_url',
            field=models.URLField(blank=True, help_text="URL of the publication's cover image", null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='isfdb_id',
            field=models.PositiveBigIntegerField(blank=True, db_index=True, help_text='ISFDB ID', null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='pages',
            field=models.CharField(blank=True, help_text='Number of pages in the publication', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='publicationseriestransliteration',
            name='transliterated_text',
            field=models.TextField(blank=True, help_text='Romanized version of the original text', null=True, verbose_name='Romanized Text'),
        ),
        migrations.AlterField(
            model_name='publishertransliteration',
            name='transliterated_text',
            field=models.TextField(blank=True, help_text='Romanized version of the original text', null=True, verbose_name='Romanized Text'),
        ),
    ]