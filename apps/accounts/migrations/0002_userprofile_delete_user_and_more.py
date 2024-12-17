# Generated by Django 5.1.4 on 2024-12-17 18:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(blank=True, help_text='Your date of birth', null=True, verbose_name='Birth Date')),
                ('country', models.CharField(blank=True, help_text='Your country of residence', max_length=100, null=True, verbose_name='Country')),
                ('bio', models.TextField(blank=True, help_text='Tell us about yourself', null=True, verbose_name='Biography')),
                ('avatar', models.URLField(blank=True, help_text='URL to your profile picture', null=True, verbose_name='Avatar URL')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['user__username'],
            },
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddIndex(
            model_name='userprofile',
            index=models.Index(fields=['user'], name='accounts_us_user_id_806298_idx'),
        ),
    ]
