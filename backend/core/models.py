from django.db import models

class Asset(models.Model):
    """
    Represents any tradable asset: stock, bond, ETF, commodity, etc.
    """
    symbol = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=50)  # e.g. 'equity', 'bond', 'commodity'
    currency = models.CharField(max_length=10, default='USD')
    # e.g. bond-specific fields can go in a BondDetails model

    def __str__(self):
        return f"{self.symbol} ({self.asset_type})"


class MarketData(models.Model):
    """
    Historical or EOD (End Of Day) market data for an Asset.
    Could also store intraday if needed.
    """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()               # or DateTimeField if intraday
    open_price = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    high_price = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    low_price = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    close_price = models.DecimalField(max_digits=20, decimal_places=6)
    volume = models.BigIntegerField(null=True, blank=True)
    source = models.CharField(max_length=50, default='unknown')  # e.g. 'Bloomberg', 'Yahoo'

    class Meta:
        unique_together = ('asset', 'date')
        indexes = [
            models.Index(fields=['asset', 'date']),
        ]

    def __str__(self):
        return f"{self.asset.symbol} on {self.date} close={self.close_price}"

class Factor(models.Model):
    """
    Defines a factor used in analytics, like 'Value', 'Momentum', or a macro index.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=50, default='style')  # e.g. style factor, macro factor

    def __str__(self):
        return self.name


class FactorValue(models.Model):
    """
    Stores factor time-series data (e.g., daily returns or factor levels).
    """
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=20, decimal_places=8)

    class Meta:
        unique_together = ('factor', 'date')
        indexes = [
            models.Index(fields=['factor', 'date']),
        ]

    def __str__(self):
        return f"{self.factor.name} on {self.date}: {self.value}"

class Portfolio(models.Model):
    """
    Represents a portfolio or strategy. Could be owned by a user.
    """
    name = models.CharField(max_length=100, unique=True)
    owner = models.CharField(max_length=50, null=True, blank=True)  
    base_currency = models.CharField(max_length=10, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PortfolioHolding(models.Model):
    """
    Current holdings of a portfolio in a specific asset.
    Could be updated each time a new transaction is processed.
    """
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=4)

    class Meta:
        unique_together = ('portfolio', 'asset')

    def __str__(self):
        return f"{self.portfolio.name} holds {self.asset.symbol}: {self.quantity}"


class Transaction(models.Model):
    """
    Logs buy/sell trades or other events (dividends, deposits).
    Negative quantity for sells, positive for buys.
    """
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    trade_date = models.DateField()
    quantity = models.DecimalField(max_digits=20, decimal_places=4)
    price = models.DecimalField(max_digits=20, decimal_places=6)
    transaction_type = models.CharField(max_length=30, default='BUY')  # SELL, DIVIDEND, etc.
    # Additional fields: fees, order_id, etc.

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tx {self.id}: {self.transaction_type} {self.quantity} of {self.asset.symbol} @ {self.price}"

class RiskMetric(models.Model):
    """
    Storing computed risk metrics (VaR, CVaR, etc.) for a portfolio on a given date.
    """
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    date = models.DateField()
    metric_type = models.CharField(max_length=50)   # e.g. 'VaR_95', 'CVaR_99', 'Volatility'
    value = models.DecimalField(max_digits=20, decimal_places=6)

    class Meta:
        indexes = [
            models.Index(fields=['portfolio', 'date', 'metric_type']),
        ]

    def __str__(self):
        return f"{self.metric_type} on {self.date} for {self.portfolio.name}: {self.value}"


class PortfolioPerformance(models.Model):
    """
    Optional: store daily or periodic returns for quick retrieval (NAV-based).
    """
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    date = models.DateField()
    nav = models.DecimalField(max_digits=20, decimal_places=6)
    daily_return = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    class Meta:
        unique_together = ('portfolio', 'date')
        indexes = [
            models.Index(fields=['portfolio', 'date']),
        ]

    def __str__(self):
        return f"{self.portfolio.name} NAV {self.nav} on {self.date}"

class Scenario(models.Model):
    scenario_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.scenario_name


class ScenarioResult(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=50)  # e.g. 'PnL', 'Drawdown'
    value = models.DecimalField(max_digits=20, decimal_places=6)

    # Possibly store date or a reference to a scenario run ID
    run_date = models.DateTimeField(auto_now_add=True)
