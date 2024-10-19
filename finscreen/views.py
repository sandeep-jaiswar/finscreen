from django.http import JsonResponse
import yfinance as yf

def get_stock_data(request, symbol):
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.info
        return JsonResponse(stock_info, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
