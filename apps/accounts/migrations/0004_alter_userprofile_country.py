# Generated by Django 5.1.4 on 2024-12-18 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, help_text='Your country of residence', max_length=50, null=True, verbose_name='Country'),
        ),
    ]
