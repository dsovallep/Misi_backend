# Generated by Django 5.1.1 on 2024-10-10 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0014_portfolioshare_total_in_fees'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioShareHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_share', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('average_price_per_share', models.DecimalField(decimal_places=2, max_digits=14)),
                ('profit_loss', models.DecimalField(decimal_places=2, max_digits=14)),
                ('total_in_fees', models.DecimalField(decimal_places=2, max_digits=14)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('portfolio_share', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investment.portfolioshare')),
            ],
        ),
    ]
