# Generated by Django 4.1.5 on 2023-01-26 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0009_alter_service_date_from_alter_service_date_to'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicecategory',
            old_name='parent_id',
            new_name='parent',
        ),
    ]
