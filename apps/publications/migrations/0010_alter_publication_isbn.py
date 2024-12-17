# Generated by Django 5.1.4 on 2024-12-16 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0009_alter_publication_publication_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='isbn',
            field=models.CharField(blank=True, help_text='ISBN-10 or ISBN-13', max_length=100, null=True),
        ),
    ]