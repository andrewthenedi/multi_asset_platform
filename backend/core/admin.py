from django.contrib import admin
from .models import (
    Asset, MarketData, Factor, FactorValue, Portfolio, 
    PortfolioHolding, Transaction, RiskMetric, PortfolioPerformance,
)

admin.site.register(Asset)
admin.site.register(MarketData)
admin.site.register(Factor)
admin.site.register(FactorValue)
admin.site.register(Portfolio)
admin.site.register(PortfolioHolding)
admin.site.register(Transaction)
admin.site.register(RiskMetric)
admin.site.register(PortfolioPerformance)
