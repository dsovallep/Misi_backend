# Generated by Django 5.1.1 on 2024-10-07 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0009_rename_price_per_share_transaction_max_price_per_share_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolioshare',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
