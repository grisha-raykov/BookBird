# Generated by Django 5.1.4 on 2024-12-15 14:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0006_title_synopsis'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Name of the series', max_length=255)),
                ('series_parent_position', models.PositiveIntegerField(blank=True, help_text='Position within the parent series', null=True)),
                ('series_note', models.TextField(blank=True, help_text='Additional notes about this series', null=True)),
                ('parent', models.ForeignKey(blank=True, help_text='Parent series if this is a subseries', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subseries', to='titles.series')),
            ],
            options={
                'verbose_name': 'Series',
                'verbose_name_plural': 'Series',
                'ordering': ['title'],
                'constraints': [models.UniqueConstraint(fields=('parent', 'series_parent_position'), name='unique_series_position')],
            },
        ),
    ]
