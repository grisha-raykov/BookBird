# Generated by Django 5.1.4 on 2024-12-18 07:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('publications', '0013_publicationtitle'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='List Name')),
                ('list_type', models.CharField(choices=[('read', 'Read'), ('currently_reading', 'Currently Reading'), ('to_read', 'Want to Read'), ('custom', 'Custom List')], default='custom', max_length=20)),
                ('is_default', models.BooleanField(default=False, help_text='Indicates if this is a default system list')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reading_lists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reading List',
                'verbose_name_plural': 'Reading Lists',
                'ordering': ['-created_at'],
                'unique_together': {('user', 'list_type')},
            },
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_entries', to='publications.publication')),
                ('reading_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='lists.readinglist')),
            ],
            options={
                'ordering': ['-added_at'],
                'unique_together': {('reading_list', 'publication')},
            },
        ),
    ]
