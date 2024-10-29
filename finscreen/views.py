from rest_framework.response import Response
from .models import Company, Sector, Industry, Exchange, Currency, Address, Officer, OfficerCompensation, CompanyFinancials, Dividend, StockPrice, RiskMetrics, PerformanceMetrics, AnalystOpinion, BalanceSheet, EsgScore
import yfinance as yf
import pandas as pd  # Import pandas here
from datetime import datetime
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework import status

def calculate_fhs(profitability_score, growth_score, valuation_score, financial_health_score, efficiency_score):
    # Weights for each metric category
    weights = {
        'profitability': 0.25,
        'growth': 0.25,
        'valuation': 0.20,
        'financial_health': 0.20,
        'efficiency': 0.10
    }

    # Calculate weighted score
    fhs = (profitability_score * weights['profitability'] +
           growth_score * weights['growth'] +
           valuation_score * weights['valuation'] +
           financial_health_score * weights['financial_health'] +
           efficiency_score * weights['efficiency'])

    # Interpretation of FHS score
    if fhs > 0.5:
        return "Strong Buy", fhs
    elif 0.2 < fhs <= 0.5:
        return "Buy", fhs
    elif -0.2 <= fhs <= 0.2:
        return "Hold", fhs
    elif -0.5 <= fhs < -0.2:
        return "Sell", fhs
    else:
        return "Strong Sell", fhs


def calculate_tts(rsi_score, ma_score, macd_score, adx_score, bollinger_score, volume_score):
    # Weights for each indicator
    weights = {
        'rsi': 0.20,
        'ma': 0.25,
        'macd': 0.15,
        'adx': 0.10,
        'bollinger': 0.10,
        'volume': 0.20
    }

    # Calculate weighted score
    tts = (rsi_score * weights['rsi'] +
           ma_score * weights['ma'] +
           macd_score * weights['macd'] +
           adx_score * weights['adx'] +
           bollinger_score * weights['bollinger'] +
           volume_score * weights['volume'])

    # Interpretation of TTS score
    if tts > 0.5:
        return "Strong Buy", tts
    elif 0.2 < tts <= 0.5:
        return "Buy", tts
    elif -0.2 <= tts <= 0.2:
        return "Hold", tts
    elif -0.5 <= tts < -0.2:
        return "Sell", tts
    else:
        return "Strong Sell", tts


def technical_score(rsi, ma_50, ma_200, macd, adx, bollinger, volume):
    score = 0
    
    # RSI scoring
    if rsi < 30:
        score += 2
    elif rsi > 70:
        score -= 2
    
    # Moving Averages scoring
    if ma_50 > ma_200:
        score += 2
    elif ma_50 < ma_200:
        score -= 2
    
    # MACD scoring
    if macd == 'bullish':
        score += 1
    elif macd == 'bearish':
        score -= 1

    # ADX scoring
    if adx > 25:
        score += 1
    elif adx < 20:
        score -= 1
    
    # Bollinger Bands scoring
    if bollinger == 'below':
        score += 1
    elif bollinger == 'above':
        score -= 1

    # Volume scoring
    if volume == 'above_average':
        score += 1
    elif volume == 'below_average':
        score -= 1

    return score



@api_view(['GET'])
def get_stock_history(request, symbol):
    ticker = yf.Ticker(symbol)
    history = ticker.history(period="1mo")
    history_json = history.to_dict('records')
    return Response(history_json)

@api_view(['GET'])
def get_stock_info(request, symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    return Response(info)

@api_view(['GET'])
def get_stock_actions(request, symbol):
    ticker = yf.Ticker(symbol)
    actions = ticker.actions
    actions_json = actions.reset_index().to_dict('records')
    return Response(actions_json)

@api_view(['GET'])
def get_stock_dividends(request, symbol):
    ticker = yf.Ticker(symbol)
    dividends = ticker.dividends
    #dividends_json = dividends.to_dict('records')
    return Response(dividends)

@api_view(['GET'])
def get_stock_splits(request, symbol):
    ticker = yf.Ticker(symbol)
    splits = ticker.splits
    splits_json = splits.to_dict()
    return Response(splits_json)

@api_view(['GET'])
def get_stock_financials(request, symbol):
    try:
        ticker = yf.Ticker(symbol)
        balance_sheet = ticker.balance_sheet

        if not balance_sheet.empty:
            for key, value in balance_sheet.items():
                value = pd.Series(value)
                if isinstance(value, (dict, pd.Series)):
                    balance_sheet_series = value.where(pd.notna(value), None).to_dict()
                    balance_sheet_dict = {
                        "date": key,
                        "cash_and_cash_equivalents": balance_sheet_series.get("Cash And Cash Equivalents"),
                        "short_term_investments": balance_sheet_series.get("Other Short Term Investments"),
                        "net_receivables": balance_sheet_series.get("Accounts Receivable"),
                        "inventory": balance_sheet_series.get("Inventory"),
                        "total_current_assets": balance_sheet_series.get("Total Assets"),
                        "long_term_investments": balance_sheet_series.get("Investments And Advances"),
                        "property_plant_equipment": balance_sheet_series.get("Net PPE"),
                        "intangible_assets": balance_sheet_series.get("Goodwill And Other Intangible Assets"),
                        "total_assets": balance_sheet_series.get("Total Assets"),
                        "total_liabilities": balance_sheet_series.get("Total Liabilities Net Minority Interest"),
                        "total_equity": balance_sheet_series.get("Stockholders Equity"),
                    }
                    return Response(balance_sheet_dict)
        else:
            return Response(
                {"error": "No balance sheet data found for this symbol."},
                status=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        return Response(
            {"error": f"An error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_stock_quarterly_financials(request, symbol):
    ticker = yf.Ticker(symbol)
    quarterly_financials = ticker.quarterly_financials
    quarterly_financials_json = quarterly_financials.to_dict()
    return Response(quarterly_financials_json)

@api_view(['GET'])
def get_stock_sustainability(request, symbol):
    ticker = yf.Ticker(symbol)
    sustainability = ticker.sustainability
    sustainability_json = sustainability.to_dict()
    return Response(sustainability_json)

@api_view(['GET'])
def get_stock_recommendations(request, symbol):
    ticker = yf.Ticker(symbol)
    recommendations = ticker.recommendations
    recommendations_json = recommendations.reset_index().to_dict('records')
    return Response(recommendations_json)

@api_view(['GET'])
def get_stock_earnings(request, symbol):
    ticker = yf.Ticker(symbol)
    earnings = ticker.earnings
    earnings_json = earnings.to_dict()
    return Response(earnings_json)

@api_view(['GET'])
def get_stock_quarterly_earnings(request, symbol):
    ticker = yf.Ticker(symbol)
    quarterly_earnings = ticker.quarterly_earnings
    quarterly_earnings_json = quarterly_earnings.to_dict()
    return Response(quarterly_earnings_json)

@api_view(['GET'])
def get_stock_major_holders(request, symbol):
    ticker = yf.Ticker(symbol)
    major_holders = ticker.major_holders
    major_holders_json = major_holders.to_dict()
    return Response(major_holders_json)

@api_view(['GET'])
def get_stock_institutional_holders(request, symbol):
    ticker = yf.Ticker(symbol)
    institutional_holders = ticker.institutional_holders
    institutional_holders_json = institutional_holders.reset_index().to_dict('records')
    return Response(institutional_holders_json)

@api_view(['GET'])
def get_stock_calendar(request, symbol):
    ticker = yf.Ticker(symbol)
    calendar = ticker.calendar
    calendar_json = calendar.to_dict()
    return Response(calendar_json)

@api_view(['GET'])
def get_stock_options(request, symbol):
    ticker = yf.Ticker(symbol)
    options = ticker.options
    return Response({'options': list(options)})

@api_view(['GET'])
def get_stock_option_chain(request, symbol, expiration):
    ticker = yf.Ticker(symbol)
    options = ticker.option_chain(expiration)
    calls_json = options.calls.reset_index().to_dict('records')
    puts_json = options.puts.reset_index().to_dict('records')
    return Response({'calls': calls_json, 'puts': puts_json})

@api_view(['GET'])
def get_stock_isin(request, symbol):
    ticker = yf.Ticker(symbol)
    isin_code = ticker.isin
    return Response({'isin': isin_code})

@api_view(['GET'])
def get_stock_news(request, symbol):
    ticker = yf.Ticker(symbol)
    news = ticker.news
    return Response({'news': news})

@api_view(['POST'])
def scrap_data(request):
    try:
        symbols = request.data.get("symbols", [])
        results = {}
        for symbol in symbols:
            symbol_responses = []
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                balance_sheet = ticker.balance_sheet
                # sustainability = ticker.sustainability.to_dict()


                with transaction.atomic():
                    sector, created = Sector.objects.get_or_create(sector_name=info.get('sector'))

                    industry, created = Industry.objects.get_or_create(industry_name=info.get('industry'))

                    exchange, created = Exchange.objects.get_or_create(exchange_name=info.get('exchange'))

                    currency, created = Currency.objects.get_or_create(currency_code=info.get('currency'))

                    company, created = Company.objects.update_or_create(
                        symbol=info.get('symbol'),
                        defaults={
                            'name': info.get('longName'),
                            'short_name': info.get('shortName'),
                            'long_name': info.get('longName'),
                            'sector_id': sector.id,
                            'industry_id': industry.id,
                            'total_employees': info.get('fullTimeEmployees'),
                            'exchange_id': exchange.id,
                            'currency_id': currency.id
                        }
                    )

                    Address.objects.update_or_create(
                        company_id=company.id,
                        defaults={
                            'address1': info.get('address1'),
                            'address2': info.get('address2'),
                            'city': info.get('city'),
                            'zip': info.get('zip'),
                            'country': info.get('country'),
                            'phone': info.get('phone'),
                            'fax': info.get('fax'),
                            'website': info.get('website'),
                        }
                    )
                    
                    StockPrice.objects.update_or_create(
                        company_id=company.id,
                        defaults={
                            'previous_close' : info.get('previousClose'),
                            'open' : info.get('open'),
                            'day_low' : info.get('dayLow'),
                            'day_high' : info.get('dayHigh'),
                            'current_price' : info.get('currentPrice'),
                            'fifty_two_week_low' : info.get('fiftyTwoWeekLow'),
                            'fifty_two_week_high' : info.get('fiftyTwoWeekHigh'),
                            'fifty_day_avg' : info.get('fiftyDayAverage'),
                            'two_hundred_day_avg' : info.get('twoHundredDayAverage'),
                            'volume' : info.get('volume'),
                            'average_volume' : info.get('averageVolume'),
                        }
                    )

                    for officer_data in info.get('companyOfficers', []):
                        officer, created = Officer.objects.update_or_create(
                            company_id=company.id,
                            name=officer_data.get('name'),
                            defaults={
                                'title': officer_data.get('title'),
                                'age': officer_data.get('age'),
                                'fiscal_year': officer_data.get('fiscalYear'),
                                'year_born': officer_data.get('yearBorn'),
                            }
                        )
                        OfficerCompensation.objects.update_or_create(
                            officer_id=officer.id,
                            defaults={
                                'total_pay': officer_data.get('totalPay', None),
                                'exercised_value': officer_data.get('exercisedValue', None),
                                'unexercised_value': officer_data.get('unexercisedValue', None),
                            }
                        )

                    CompanyFinancials.objects.update_or_create(
                        company_id=company.id,
                        defaults={
                            'market_cap': info.get('marketCap'),
                            'enterprise_value': info.get('enterpriseValue'),
                            'total_cash': info.get('totalCash'),
                            'total_debt': info.get('totalDebt'),
                            'total_revenue': info.get('totalRevenue'),
                            'revenue_per_share': info.get('revenuePerShare'),
                            'gross_margin': info.get('grossMargins'),
                            'ebitda_margin': info.get('ebitdaMargins'),
                            'operating_margin': info.get('operatingMargins'),
                            'profit_margin': info.get('profitMargins'),
                            'book_value': info.get('bookValue'),
                            'debt_to_equity_ratio': info.get('debtToEquity'),
                            'current_ratio': info.get('currentRatio'),
                            'quick_ratio': info.get('quickRatio'),
                            'free_cashflow': info.get('freeCashflow'),
                            'operating_cashflow': info.get('operatingCashflow'),
                            'currency_id': currency.id,
                        }
                    )

                    Dividend.objects.update_or_create(
                        company_id=company.id,
                        defaults={
                            'dividend_rate': info.get('dividendRate'),
                            'dividend_yield': info.get('dividendYield'),
                            'payout_ratio': info.get('payoutRatio'),
                            'ex_dividend_date': datetime.fromtimestamp(info.get('exDividendDate')) if info.get('exDividendDate') else None,
                            'five_year_avg_dividend_yield': info.get('fiveYearAvgDividendYield'),
                            'trailing_annual_dividend_rate': info.get('trailingAnnualDividendRate'),
                            'trailing_annual_dividend_yield': info.get('trailingAnnualDividendYield'),
                        }
                    )

                    RiskMetrics.objects.update_or_create(
                        company_id=company.id,
                        defaults={
                            'audit_risk': info.get('auditRisk'),
                            'board_risk': info.get('boardRisk'),
                            'compensation_risk': info.get('compensationRisk'),
                            'shareholder_rights_risk': info.get('shareholderRightsRisk'),
                            'overall_risk': info.get('overallRisk'),
                        }
                    )
                    
                    # EsgScore.objects.update_or_create(
                    #     company_id=company.id,
                    #     defaults={
                    #         'environmental_score': sustainability.get('environmentalScore'),
                    #         'social_score': sustainability.get('socialScore'),
                    #         'governance_score': sustainability.get('governanceScore'),
                    #         'total_esg_score': sustainability.get('totalEsg'),
                    #         'esg_rating': sustainability.get('esgPerformance'),
                    #     }
                    # )

                    if not balance_sheet.empty:
                        for key, value in balance_sheet.items():
                            value = pd.Series(value)
                            if isinstance(value, (dict, pd.Series)):
                                balance_sheet_series = value.where(pd.notna(value), None).to_dict()
                                balance_sheet_dict = {
                                    "date": key,
                                    "cash_and_cash_equivalents": balance_sheet_series.get("Cash And Cash Equivalents"),
                                    "short_term_investments": balance_sheet_series.get("Other Short Term Investments"),
                                    "net_receivables": balance_sheet_series.get("Accounts Receivable"),
                                    "inventory": balance_sheet_series.get("Inventory"),
                                    "total_current_assets": balance_sheet_series.get("Total Assets"),
                                    "long_term_investments": balance_sheet_series.get("Investments And Advances"),
                                    "property_plant_equipment": balance_sheet_series.get("Net PPE"),
                                    "intangible_assets": balance_sheet_series.get("Goodwill And Other Intangible Assets"),
                                    "total_assets": balance_sheet_series.get("Total Assets"),
                                    "total_liabilities": balance_sheet_series.get("Total Liabilities Net Minority Interest"),
                                    "total_equity": balance_sheet_series.get("Stockholders Equity"),
                                }

                                BalanceSheet.objects.update_or_create(
                                    company_id=company.id,
                                    defaults=balance_sheet_dict
                                )

            except Exception as e:
                symbol_responses.append({"error": str(e)})

            results[symbol] = symbol_responses

        return Response({'status': 'success', 'message': 'Data scraped and inserted successfully', 'data': results})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)

