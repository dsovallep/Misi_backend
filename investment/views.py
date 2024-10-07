from rest_framework import viewsets
from .models import Portfolio, Share, Transaction, PortfolioShare
from .serializers import PortfolioSerializer, ShareSerializer, TransactionSerializer, PortfolioShareSerializer


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


class ShareViewSet(viewsets.ModelViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class PortfolioShareViewSet(viewsets.ModelViewSet):
    queryset = PortfolioShare.objects.all()
    serializer_class = PortfolioShareSerializer


