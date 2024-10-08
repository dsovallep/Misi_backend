from rest_framework import serializers
from .models import Portfolio, Share, Transaction, PortfolioShare


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
        fields = '__all__'
        read_only_fields = ('total_transaction',)  # Make total_transaction read-only


class PortfolioShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioShare
        fields = '__all__'
