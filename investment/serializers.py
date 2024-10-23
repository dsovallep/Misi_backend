from rest_framework import serializers
from .models import Portfolio, Share, Transaction, PortfolioShare, PortfolioShareHistory


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = ['id', 'symbol', 'name', 'exchange', 'current_price']


class TransactionSerializer(serializers.ModelSerializer):
    share_name = serializers.CharField(source='share_id.name', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'portfolio_id', 'share_id', 'share_name', 'transaction_type', 'quantity', 'max_price_per_share', 'total_shares_price', 'fees', 'total_transaction', 'transaction_date', 'orden_number', 'created_at']
        read_only_fields = ('total_transaction', 'created_at', 'share_name', ) 
    

class PortfolioShareSerializer(serializers.ModelSerializer):
    share_name = serializers.CharField(source='share_id.name', read_only=True)
    share_symbol = serializers.CharField(source='share_id.symbol', read_only=True)

    class Meta:
        model = PortfolioShare
        fields = ['id', 'share_symbol', 'share_name', 'number_share', 'amount', 'average_price_per_share', 'profit_loss', 'total_in_fees']


class  PortfolioShareHistorySerializer(serializers.ModelSerializer):
    share_name = serializers.CharField(source='portfolio_share.share_id.name', read_only=True)
    class Meta:
        model = PortfolioShareHistory
        fields = ['id', 'share_name', 'transaction_type', 'number_share', 'total_shares_price', 'amount', 'average_price_per_share', 'profit_loss', 'total_in_fees']
