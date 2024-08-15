# Generated by Django 5.1 on 2024-08-14 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_song_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ['id']},
        ),
        migrations.AddIndex(
            model_name='song',
            index=models.Index(fields=['id'], name='api_song_id_5a3a7c_idx'),
        ),
    ]
