from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PortfolioViewSet, ShareViewSet, TransactionViewSet, PortfolioShareViewSet

router = DefaultRouter()
router.register(r'portfolio', PortfolioViewSet)
router.register(r'share', ShareViewSet)
router.register(r'transaction', TransactionViewSet)
router.register(r'portfolioshare', PortfolioShareViewSet)

urlpatterns = [
            path('', include(router.urls)),
        ]

