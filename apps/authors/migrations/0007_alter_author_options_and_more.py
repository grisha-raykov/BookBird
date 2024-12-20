# Generated by Django 5.1.4 on 2024-12-17 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0006_alter_authortransliteration_options_and_more'),
        ('languages', '0004_alter_language_native_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'canonical_name'], 'verbose_name': 'Author', 'verbose_name_plural': 'Authors'},
        ),
        migrations.AddIndex(
            model_name='author',
            index=models.Index(fields=['last_name'], name='authors_aut_last_na_13323b_idx'),
        ),
        migrations.AddIndex(
            model_name='author',
            index=models.Index(fields=['canonical_name'], name='authors_aut_canonic_49d541_idx'),
        ),
    ]
