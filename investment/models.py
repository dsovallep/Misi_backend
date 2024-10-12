import logging
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


logger = logging.getLogger(__name__)


class Portfolio(models.Model):
    """
    Represents a user's investment portfolio.

    Attributes:
        user_id: Foreign key to the User model.
        name: Name of the portfolio.
        description: Optional text field to describe the portfolio.
        created_at: Timestamp when the portfolio was created.
        updated_at: Timestamp when the portfolio was last updated.
    """

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({str(self.user_id.username)})"


class Share(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    exchange = models.CharField(max_length=50, default='Unknown')
    current_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class Transaction(models.Model):
    """                                                                                                 Represents a user's investment Transaction.
    
    Attributes:
        
    """

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
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to calculate the total transaction amount.

        Logs relevant transaction details and updates the portfolio-share relationship.
        """
        
        try:
            self.total_transaction = self.total_shares_price + self.fees
            super(Transaction, self).save(*args, **kwargs)
            self.update_portfolio_share()
        
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            ValidationError(f'Unexpected error: {e}')
            raise 
    
    @staticmethod
    def create_portfolio_share_history(portfolio_share, transaction_type, number_share, total_shares_price, amount, average_price_per_share, profit_loss, total_in_fees):
        """
        Create a object of PortfolioShareHistory.
        """ 
        
        PortfolioShareHistory.objects.create(
        portfolio_share=portfolio_share,
        transaction_type=transaction_type,
        number_share=number_share,
        total_shares_price = total_shares_price,
        amount=amount,
        average_price_per_share=average_price_per_share,
        profit_loss=profit_loss,
        total_in_fees=total_in_fees
        )
    
    def update_portfolio_share(self):
        """
        Update the portfolio share based on the transaction.
        """
    
        portfolio_share, created = PortfolioShare.objects.get_or_create(
                portfolio_id=self.portfolio_id, share_id=self.share_id
        ) 

        # Store the current state in the model PortfolioShareHistory before updating
        self.create_portfolio_share_history(portfolio_share,
        portfolio_share.last_transaction_type,
        portfolio_share.number_share,
        portfolio_share.total_shares_price,
        portfolio_share.amount,
        portfolio_share.average_price_per_share,
        portfolio_share.profit_loss,
        portfolio_share.total_in_fees
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
            if self.total_shares_price <= portfolio_share.profit_loss:
                portfolio_share.profit_loss = portfolio_share.profit_loss - self.total_shares_price
            else:
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
        portfolio_share.save()
        
        self.create_portfolio_share_history(
        portfolio_share,
        portfolio_share.last_transaction_type,
        portfolio_share.number_share,
        portfolio_share.total_shares_price,
        portfolio_share.amount,
        portfolio_share.average_price_per_share,
        portfolio_share.profit_loss,
        portfolio_share.total_in_fees
        )


    def __str__(self):
        return f"{self.transaction_type} {self.quantity} shares of {self.share_id.symbol} in {self.portfolio_id.name}"


class PortfolioShare (models.Model):
    """
    Represent the current state of a share in a portfolio.
    """

    TRANSACTION_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    
    portfolio_id = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    share_id = models.ForeignKey(Share, on_delete=models.CASCADE)
    last_transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=4, default='BUY')
    number_share = models.IntegerField(default=0) 
    total_shares_price = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal(0.00))
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal(0.00)) 
    average_price_per_share = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    profit_loss = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, default=Decimal(0.00))
    total_in_fees = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, default=Decimal(0.00))
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.number_share} shares of {self.share_id.symbol} in {self.portfolio_id.name} at average price {self.average_price_per_share}"


class PortfolioShareHistory(models.Model):
    """
    Represent the history of changes to a portfolio share.
    """

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
