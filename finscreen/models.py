from django.db import models

# 1. Sector Table
class Sector(models.Model):
    id = models.AutoField(primary_key=True)
    sector_name = models.CharField(max_length=255)
    class Meta:
        db_table = 'sector'

# 2. Industry Table
class Industry(models.Model):
    id = models.AutoField(primary_key=True)
    industry_name = models.CharField(max_length=255)
    class Meta:
        db_table = 'industry'


# 3. Exchange Table
class Exchange(models.Model):
    id = models.AutoField(primary_key=True)
    exchange_name = models.CharField(max_length=255)
    class Meta:
        db_table = 'exchange'


# 4. Currency Table
class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    currency_code = models.CharField(max_length=10)
    currency_name = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        db_table = 'currency'


# 5. Company Table
class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=50, null=True, blank=True)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    long_name = models.CharField(max_length=255, null=True, blank=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)
    founded = models.IntegerField(null=True, blank=True)  # YEAR data type not available, use IntegerField
    total_employees = models.IntegerField(null=True, blank=True)
    exchange = models.ForeignKey(Exchange, on_delete=models.SET_NULL, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'company'


# 6. Address Table
class Address(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    fax = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'address'


# 7. Officer Table
class Officer(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    fiscal_year = models.IntegerField(null=True, blank=True)  # YEAR type stored as Integer
    year_born = models.IntegerField(null=True, blank=True)  # YEAR type stored as Integer
    class Meta:
        db_table = 'officer'


# 8. Officer Compensation Table
class OfficerCompensation(models.Model):
    id = models.AutoField(primary_key=True)
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE)
    total_pay = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    exercised_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    unexercised_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = 'officer_compensation'


# 9. Company Financials Table
class CompanyFinancials(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    market_cap = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    enterprise_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_cash = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_debt = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    revenue_per_share = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    gross_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ebitda_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    operating_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    book_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    debt_to_equity_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    current_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    quick_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    free_cashflow = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    operating_cashflow = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = 'company_financials'


# 10. Dividend Table
class Dividend(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    dividend_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dividend_yield = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    payout_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ex_dividend_date = models.DateField(null=True, blank=True)
    five_year_avg_dividend_yield = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    trailing_annual_dividend_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    trailing_annual_dividend_yield = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = 'dividend'


# 11. Stock Price Table
class StockPrice(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    previous_close = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    open = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    day_low = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    day_high = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    current_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    fifty_two_week_low = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    fifty_two_week_high = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    fifty_day_avg = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    two_hundred_day_avg = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    volume = models.BigIntegerField(null=True, blank=True)
    average_volume = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = 'stock_price'


# 12. Risk Metrics Table
class RiskMetrics(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    audit_risk = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    board_risk = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    compensation_risk = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    shareholder_rights_risk = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    overall_risk = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = 'risk_metrics'

# 13. Performance Metrics Table
class PerformanceMetrics(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    week_52_change = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sp500_week_52_change = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    beta = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    trailing_pe = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    forward_pe = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    peg_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    price_to_sales_ratio = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    price_to_book_ratio = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    enterprise_value_to_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    enterprise_value_to_ebitda = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = 'performance_metrics'

class AnalystOpinion(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    target_price_high = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    target_price_low = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    target_price_mean = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    target_price_median = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    recommendation_key = models.CharField(max_length=50, null=True, blank=True)
    number_of_analysts = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'analyst_opinion'

class FundamentalIndicator(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    return_on_equity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    return_on_assets = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    gross_profit_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    net_profit_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pb_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ev_to_ebitda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_to_cashflow = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    asset_turnover = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    inventory_turnover = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = 'fundamental_indicator'

class GrowthMetric(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    revenue_growth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    earnings_growth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    eps_growth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dividend_growth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    book_value_growth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = 'growth_metric'

class BalanceSheet(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    cash_and_cash_equivalents = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    short_term_investments = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_receivables = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    inventory = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_current_assets = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    long_term_investments = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    property_plant_equipment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    intangible_assets = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_liabilities = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_equity = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = "balance_sheet"
        
class EsgScore(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='esg_scores')
    environmental_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    social_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    governance_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_esg_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    esg_rating = models.CharField(max_length=50, null=True, blank=True)
    rating_agency = models.CharField(max_length=255, null=True, blank=True)
    last_updated = models.DateField(null=True, blank=True, auto_now_add=True)

    class Meta:
        db_table = 'esg_score'
