from rest_framework import serializers
from .models import Portfolio, Share, Transaction, PortfolioShare, PortfolioShareHistory


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'portfolio_id', 'share_id', 'transaction_type', 'quantity', 'max_price_per_share', 'total_shares_price', 'fees', 'total_transaction', 'transaction_date', 'orden_number']
        read_only_fields = ('total_transaction', ) 
    

class PortfolioShareSerializer(serializers.ModelSerializer):
    share_name = serializers.CharField(source='share_id.name', read_only=True)
    class Meta:
        model = PortfolioShare
        fields = ['id', 'share_name', 'number_share', 'amount', 'average_price_per_share', 'profit_loss', 'total_in_fees']


class  PortfolioShareHistorySerializer(serializers.ModelSerializer):
    share_name = serializers.CharField(source='portfolio_share.share_id.name', read_only=True)
    class Meta:
        model = PortfolioShareHistory
        fields = ['id', 'share_name', 'transaction_type', 'number_share', 'total_shares_price', 'amount', 'average_price_per_share', 'profit_loss', 'total_in_fees']
