# Generated by Django 5.1.2 on 2024-11-09 17:25

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textpad', '0002_rename_document_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
