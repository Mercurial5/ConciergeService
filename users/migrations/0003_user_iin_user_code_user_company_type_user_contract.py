# Generated by Django 4.1.5 on 2023-01-25 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='IIN',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='code',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='company_type',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='contract',
            field=models.FileField(null=True, upload_to='media/contracts/'),
        ),
    ]
