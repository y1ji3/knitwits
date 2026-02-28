

from django.shortcuts import render
from .models import Shop

def dashboard(request):
    stores = Shop.objects.all().order_by('shop_name')
    return render(request, 'dashboard.html', {'stores': stores})

def low_stock(request): #returns a list of items with low stock (5 or less)
    low_stock_items = Shop.objects.filter(shop_stock__lte=5).order_by('shop_name')
    return render(request, 'low_stock.html', {'low_stock_items': low_stock_items})

def out_of_stock(request): #returns a list of items that are out of stock (stock = 0)
    out_of_stock_items = Shop.objects.filter(shop_stock=0).order_by('shop_name')
    return render(request, 'out_of_stock.html', {'out_of_stock_items': out_of_stock_items})

def all_pick_list(request): #returns a list of items that need to be picked (stock 5 or less)
    pick_list_items = Shop.objects.filter(shop_stock__lte=5).order_by('shop_name')
    return render(request, 'pick_list.html', {'pick_list_items': pick_list_items})

