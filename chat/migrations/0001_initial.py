# Generated by Django 4.1.5 on 2023-01-24 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collocutor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chats', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chats_manager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
