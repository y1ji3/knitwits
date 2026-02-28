

from django.shortcuts import render
from django.db.models import Sum, Count
from .models import Shop, ShopInventory

def dashboard(request):
    stores = Shop.objects.annotate(shop_stock=Sum('inventory__stock')).order_by('name')
    return render(request, 'dashboard.html', {'stores': stores})

def low_stock(request): #returns a list of items with low stock (5 or less)
    low_stock_items = ShopInventory.objects.select_related('shop', 'product').filter(stock__lte=5).order_by('shop__name', 'product__name')
    return render(request, 'low_stock.html', {'low_stock_items': low_stock_items})

def out_of_stock(request): #returns a list of items that are out of stock (stock = 0)
    out_of_stock_items = ShopInventory.objects.select_related('shop', 'product').filter(stock=0).order_by('shop__name', 'product__name')
    return render(request, 'out_of_stock.html', {'out_of_stock_items': out_of_stock_items})

def all_pick_list(request): #returns a list of items that need to be picked (stock 5 or less)
    pick_list_items = ShopInventory.objects.select_related('shop', 'product').filter(stock__lte=5).order_by('shop__name', 'product__name').values_list('shop__name', 'product__name', 'product__variant', 'stock')
    print("Pick List Items:")
    print(list(pick_list_items))
    return render(request, 'pick_list.html', {'pick_list_items': pick_list_items})

def notifications(request):
    low_stock_by_store = (
        ShopInventory.objects
        .filter(stock__lte=5)
        .values('shop__name')
        .annotate(item_count=Count('id'))
        .order_by('shop__name')
    )

    if low_stock_by_store:
        store_name = low_stock_by_store[0]['shop__name']
        item_count = low_stock_by_store[0]['item_count']
    else:
        store_name = 'Main'
        item_count = 0

    return render(request, 'notifications.html', {'store_name': store_name, 'item_count': item_count})
   