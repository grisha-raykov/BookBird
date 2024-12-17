# Generated by Django 5.1.4 on 2024-12-17 09:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0005_award'),
        ('titles', '0021_title_popularity_score_alter_title_isfdb_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TitleAward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isfdb_id', models.PositiveBigIntegerField(blank=True, db_index=True, help_text='ISFDB ID', null=True, unique=True)),
                ('award', models.ForeignKey(help_text='Award given to this title', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='title_awards', to='awards.award')),
                ('title', models.ForeignKey(help_text='Title that received the award', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='awards', to='titles.title')),
            ],
            options={
                'verbose_name': 'Title Award',
                'verbose_name_plural': 'Title Awards',
                'ordering': ['award__type', 'award__year'],
                'indexes': [models.Index(fields=['isfdb_id'], name='awards_titl_isfdb_i_af1a08_idx'), models.Index(fields=['award'], name='awards_titl_award_i_a38f0b_idx'), models.Index(fields=['title'], name='awards_titl_title_i_eb09b4_idx')],
            },
        ),
    ]