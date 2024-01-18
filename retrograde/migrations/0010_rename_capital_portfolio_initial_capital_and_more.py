# Generated by Django 4.0.2 on 2024-01-05 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retrograde', '0009_user_timezone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='portfolio',
            old_name='capital',
            new_name='initial_capital',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='now_datetime',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
