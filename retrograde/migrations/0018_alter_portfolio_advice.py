# Generated by Django 4.0.2 on 2024-01-08 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retrograde', '0017_portfolio_advice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='advice',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
