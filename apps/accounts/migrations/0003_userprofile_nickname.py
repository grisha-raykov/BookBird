# Generated by Django 5.1.4 on 2024-12-17 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_delete_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='nickname',
            field=models.CharField(blank=True, help_text='Your preferred display name', max_length=50, null=True, unique=True, verbose_name='Nickname'),
        ),
    ]