from django.db import models
from django.contrib.auth.models import User


class Portfolio(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Share(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    exchange = models.CharField(max_length=50, default='Unknown')
    current_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    portfolio_id = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    share_id = models.ForeignKey(Share, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    quatity = models.IntegerField()
    price_per_share = models.DecimalField(max_digits=14, decimal_places=2)
    total_share_price = models.DecimalField(max_digits=14, decimal_places=2)
    fees = models.DecimalField(max_digits=14, decimal_places=2)
    transaction_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)

class PortfolioShare (models.Model):
    portfolio_id = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    share_id = models.ForeignKey(Share, on_delete=models.CASCADE)
    number_share = models.IntegerField()
    amount = models.DecimalField(max_digits=14, decimal_places=2)
