from django.http import JsonResponse
from nsetools import Nse

def get_stock_data(request, symbol):
    nse = Nse()
    try:
        stock_data = nse.get_quote(symbol)
        return JsonResponse(stock_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
