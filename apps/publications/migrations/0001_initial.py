# Generated by Django 5.1.4 on 2024-12-16 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(help_text='Name of the publisher')),
                ('slug', models.SlugField(blank=True, help_text='Slug for the publisher', max_length=255, unique=True)),
                ('website', models.URLField(blank=True, help_text="Publisher's website URL", null=True)),
                ('isfdb_id', models.PositiveBigIntegerField(blank=True, db_index=True, help_text='ISFDB publisher ID', null=True, unique=True)),
            ],
        ),
    ]