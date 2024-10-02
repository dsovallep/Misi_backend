from django.contrib import admin
from .models import Portfolio, Share, Transaction, PortfolioShare

admin.site.register(Portfolio)
admin.site.register(Share)
admin.site.register(Transaction)
admin.site.register(PortfolioShare)

