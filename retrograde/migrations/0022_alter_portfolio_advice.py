# Generated by Django 5.0.1 on 2024-01-27 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retrograde', '0021_portfolio_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='advice',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
