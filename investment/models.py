import logging
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)


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
    quantity = models.IntegerField()
    max_price_per_share = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    total_shares_price = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal(0.00))
    fees = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal(0.00))
    total_transaction = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    transaction_date = models.DateField()
    orden_number = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        try:
            self.total_transaction = self.total_shares_price + self.fees
            # Call the original save method to preseve normal behavior
            super(Transaction, self).save(*args, **kwargs)
            self.update_portfolio_share()
        
        except Exception as e:
            raise ValidationError(f'Exception: {e}')

    def update_portfolio_share(self):
        # Fetch the PortfolioShare for the given portfolio and share, or create a new one
        # if it doesn't exist
        portfolio_share, created = PortfolioShare.objects.get_or_create(
                portfolio_id=self.portfolio_id, share_id=self.share_id
        ) 

        # Store the current state before updating
        PortfolioShareHistory.objects.create(portfolio_share=portfolio_share,
        transaction_type=portfolio_share.last_transaction_type,
        number_share=portfolio_share.number_share,
        total_shares_price = portfolio_share.total_shares_price,
        amount=portfolio_share.amount,
        average_price_per_share=portfolio_share.average_price_per_share,
        profit_loss=portfolio_share.profit_loss,
        total_in_fees=portfolio_share.total_in_fees
        )

        if self.transaction_type == 'BUY':
            
            # Update the number of shares and the total amount (price of shares + fees)
            new_total_shares = portfolio_share.number_share + self.quantity
            new_total_amount = portfolio_share.amount + self.total_shares_price

            # Calculate the new average price per share
            if new_total_shares > 0:
                new_average_price = new_total_amount / new_total_shares
            else: 
                new_average_price = 0

            # Update the portfolio share
            portfolio_share.last_transaction_type = self.transaction_type
            portfolio_share.number_share = new_total_shares
            portfolio_share.total_shares_price = self.total_shares_price
            portfolio_share.amount = new_total_amount
            portfolio_share.average_price_per_share = new_average_price
            portfolio_share.profit_loss = portfolio_share.profit_loss + self.total_shares_price

        elif self.transaction_type == 'SELL':
            if self.quantity > portfolio_share.number_share:
                raise ValidationError("Cannot sell more shares than currently held in the portfolio")

            portfolio_share.last_transaction_type = self.transaction_type
            portfolio_share.total_shares_price = self.total_shares_price

            # Update the number of shares and adjust the amount
            portfolio_share.number_share -= self.quantity
            
            #Calculate profit or loss on the sale
            portfolio_share.profit_loss = self.total_shares_price - portfolio_share.profit_loss
            
            # The amount remains the same (don't update the average price on a sell)
            if portfolio_share.number_share == 0:
                # If all shares are sold, reset the amount and average price
                portfolio_share.amount = 0
                portfolio_share.average_price_per_share = 0

            else:
                # Adjust the total amoutn based on the sold share
                portfolio_share.amount -= self.total_shares_price
        
        portfolio_share.total_in_fees += self.fees
        # Save the updated PortfolioShare
        portfolio_share.save()
        
        PortfolioShareHistory.objects.create(
        portfolio_share=portfolio_share,
        transaction_type=self.transaction_type,
        number_share=portfolio_share.number_share,
        total_shares_price = self.total_shares_price,
        amount=portfolio_share.amount,
        average_price_per_share=portfolio_share.average_price_per_share,
        profit_loss=portfolio_share.profit_loss,
        total_in_fees=portfolio_share.total_in_fees
        )

        logger.debug("Portfolio share updated successfully.")

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} shares of {self.share_id.symbol} in {self.portfolio_id.name}"


class PortfolioShare (models.Model):
    TRANSACTION_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    portfolio_id = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    share_id = models.ForeignKey(Share, on_delete=models.CASCADE)
    last_transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=4, default='BUY')
    number_share = models.IntegerField(default=0) # Total number of shares held
    total_shares_price = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal(0.00))
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal(0.00)) # Total amount invested
    average_price_per_share = models.DecimalField(max_digits=14, decimal_places=2, default=0.00) # Average cost per share
    profit_loss = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, default=Decimal(0.00))
    total_in_fees = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, default=Decimal(0.00))
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.number_share} shares of {self.share_id.symbol} in {self.portfolio_id.name} at average price {self.average_price_per_share}"


class PortfolioShareHistory(models.Model):
    TRANSACTION_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    portfolio_share = models.ForeignKey(PortfolioShare, on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=4, default='BUY')
    number_share = models.IntegerField()
    total_shares_price = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal(0.00))
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    average_price_per_share = models.DecimalField(max_digits=14, decimal_places=2)
    profit_loss = models.DecimalField(max_digits=14, decimal_places=2)
    total_in_fees = models.DecimalField(max_digits=14, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of {self.portfolio_share} at {self.created_at}"
