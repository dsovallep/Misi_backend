from django.db import models
from django.contrib.auth.models import User


class Portfolio(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.user_id.username})"


class Share(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    exchange = models.CharField(max_length=50, default='Unknown')
    current_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"


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
    total_transaction = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    transaction_date = models.DateField()
    orden_number = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_type} {self.quatity} shares of {self.share_id.symbol} in {self.portfolio_id.name}"


class PortfolioShare (models.Model):
    portfolio_id = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    share_id = models.ForeignKey(Share, on_delete=models.CASCADE)
    number_share = models.IntegerField()
    amount = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"{self.number_share} shares of {self.share_id.symbol} in {self.portfolio_id.name}"
    
