# Generated by Django 4.1.5 on 2023-01-26 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_alter_document_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documenttype',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
