# Generated by Django 5.0.6 on 2024-06-15 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audio_analysis', '0003_alter_audioanalysis_sentiment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audioanalysis',
            name='analysis_time',
        ),
    ]
