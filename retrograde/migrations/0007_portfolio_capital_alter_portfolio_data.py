# Generated by Django 4.0.2 on 2024-01-05 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retrograde', '0006_rename_cash_portfolio_data_delete_assetrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='capital',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='data',
            field=models.JSONField(blank=True, default={'records: []'}),
        ),
    ]
