

from django.shortcuts import render
from django.db.models import Sum
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
    low_stock_location_names = (
        ShopInventory.objects
        .filter(stock__gt=0, stock__lte=5)
        .values_list('shop__name', flat=True)
        .distinct()
        .order_by('shop__name')
    )
    out_of_stock_location_names = (
        ShopInventory.objects
        .filter(stock=0)
        .values_list('shop__name', flat=True)
        .distinct()
        .order_by('shop__name')
    )

    context = {
        'low_stock_location_names': low_stock_location_names,
        'out_of_stock_location_names': out_of_stock_location_names,
    }
    return render(request, 'notifications.html', context)
   