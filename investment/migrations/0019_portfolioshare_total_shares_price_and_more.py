# Generated by Django 5.1.1 on 2024-10-10 15:50

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0018_portfolioshare_last_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolioshare',
            name='total_shares_price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=14),
        ),
        migrations.AddField(
            model_name='portfoliosharehistory',
            name='total_shares_price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=14),
        ),
    ]
