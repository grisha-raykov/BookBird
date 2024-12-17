# Generated by Django 5.1.4 on 2024-12-17 04:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0005_authorpseudonym'),
        ('publications', '0010_alter_publication_isbn'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(help_text='Author of the publication', on_delete=django.db.models.deletion.CASCADE, related_name='publication_relationships', to='authors.author')),
                ('publication', models.ForeignKey(help_text='Publication by this author', on_delete=django.db.models.deletion.CASCADE, related_name='author_relationships', to='publications.publication')),
            ],
            options={
                'verbose_name': 'Publication Author',
                'verbose_name_plural': 'Publication Authors',
            },
        ),
        migrations.AddField(
            model_name='publication',
            name='authors',
            field=models.ManyToManyField(help_text='Author/s of the publication', related_name='publications', through='publications.PublicationAuthor', to='authors.author'),
        ),
        migrations.AddIndex(
            model_name='publicationauthor',
            index=models.Index(fields=['author'], name='publication_author__662f21_idx'),
        ),
        migrations.AddIndex(
            model_name='publicationauthor',
            index=models.Index(fields=['publication'], name='publication_publica_5b0421_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='publicationauthor',
            unique_together={('author', 'publication')},
        ),
    ]