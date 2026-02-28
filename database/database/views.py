

import time

from django.shortcuts import render, redirect
from django.db.models import Sum, F, ExpressionWrapper, IntegerField, Case, When, Value

from .models import Shop, ShopInventory, TierThreshold

def dashboard(request):
    stores = Shop.objects.annotate(shop_stock=Sum('inventory__stock')).order_by('name')
    return render(request, 'dashboard.html', {'stores': stores})

def low_stock(request): #returns a list of items with low stock (5 or less)
    low_stock_items = ShopInventory.objects.select_related('shop', 'product').filter(stock__lte=5).order_by('shop__name', 'product__name')
    return render(request, 'low_stock.html', {'low_stock_items': low_stock_items})

def out_of_stock(request): #returns a list of items that are out of stock (stock = 0)
    out_of_stock_items = ShopInventory.objects.select_related('shop', 'product').filter(stock=0).order_by('shop__name', 'product__name')
    return render(request, 'out_of_stock.html', {'out_of_stock_items': out_of_stock_items})

def all_pick_list(request): #returns a list of items that need to be picked (stock 4 or less)
    sort = request.GET.get('sort')
    selected_shop_id = request.GET.get('shop')

    if sort == 'shop':
        ordering = ('shop__name', 'product__name')
    else:
        ordering = ('product__name', 'shop__name')

    stores = Shop.objects.order_by('name')
    global_thresholds = TierThreshold.objects.order_by('id').first()
    xs_thresh = global_thresholds.xs_thresh if global_thresholds else 4
    s_thresh = global_thresholds.s_thresh if global_thresholds else 4
    m_thresh = global_thresholds.m_thresh if global_thresholds else 4
    l_thresh = global_thresholds.l_thresh if global_thresholds else 2
    xl_thresh = global_thresholds.xl_thresh if global_thresholds else 2

    base_queryset = ShopInventory.objects.select_related('shop', 'product')
    if selected_shop_id:
        base_queryset = base_queryset.filter(shop_id=selected_shop_id)

    pick_list_items = (
        base_queryset
        .annotate(
            target_threshold=Case(
                When(product__variant__istartswith='XS', then=Value(xs_thresh)),
                When(product__variant__istartswith='X-Small', then=Value(xs_thresh)),
                When(product__variant__istartswith='XL', then=Value(xl_thresh)),
                When(product__variant__istartswith='X-Large', then=Value(xl_thresh)),
                When(product__variant__istartswith='S', then=Value(s_thresh)),
                When(product__variant__istartswith='Small', then=Value(s_thresh)),
                When(product__variant__istartswith='M', then=Value(m_thresh)),
                When(product__variant__istartswith='Medium', then=Value(m_thresh)),
                When(product__variant__istartswith='L', then=Value(l_thresh)),
                When(product__variant__istartswith='Large', then=Value(l_thresh)),
                default=Value(4),
                output_field=IntegerField(),
            )
        )
        .annotate(pull_needed=ExpressionWrapper(F('target_threshold') - F('stock'), output_field=IntegerField()))
        .filter(pull_needed__gt=0)
        .order_by(*ordering)
    )

    # print("Pick List Items:")
    # print(list(pick_list_items))

    total_by_product = (
        pick_list_items
        .values('product__name', 'product__variant')
        .annotate(
            total_pull=Sum('pull_needed'),
            total_stock=Sum('stock')
        )
        .order_by('product__name')
    )

    response = render(request, 'pick_list.html', {
        'pick_list_items': pick_list_items,
        'total_by_product': total_by_product,
        'current_sort': sort,
        'stores': stores,
        'selected_shop_id': selected_shop_id,
    })
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

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


def thresholds(request):
    thresholds_row = TierThreshold.objects.order_by('id').first()
    saved = request.GET.get('saved') == '1'
    default_values = {
        'xs_thresh': thresholds_row.xs_thresh if thresholds_row else 4,
        's_thresh': thresholds_row.s_thresh if thresholds_row else 4,
        'm_thresh': thresholds_row.m_thresh if thresholds_row else 4,
        'l_thresh': thresholds_row.l_thresh if thresholds_row else 2,
        'xl_thresh': thresholds_row.xl_thresh if thresholds_row else 2,
    }
    save_error = None

    if request.method == 'POST':
        defaults = {
            'xs_thresh': int(request.POST.get('xs_thresh', 4) or 4),
            's_thresh': int(request.POST.get('s_thresh', 4) or 4),
            'm_thresh': int(request.POST.get('m_thresh', 4) or 4),
            'l_thresh': int(request.POST.get('l_thresh', 2) or 2),
            'xl_thresh': int(request.POST.get('xl_thresh', 2) or 2),
        }

        all_rows = list(TierThreshold.objects.order_by('id'))

        if all_rows:
            for row in all_rows:
                for key, value in defaults.items():
                    setattr(row, key, value)
                row.save()
            default_values = defaults
            if 'refresh_calculations' in request.POST:
                return redirect(f'/pick-list/?refreshed={int(time.time())}')
            return redirect('/thresholds/?saved=1')

        first_shop = Shop.objects.order_by('name').first()
        if first_shop:
            TierThreshold.objects.create(shop=first_shop, **defaults)
            default_values = defaults
            if 'refresh_calculations' in request.POST:
                return redirect(f'/pick-list/?refreshed={int(time.time())}')
            return redirect('/thresholds/?saved=1')
        save_error = 'Add at least one store before saving thresholds.'

    context = {
        'threshold_values': default_values,
        'save_error': save_error,
        'saved': saved,
    }
    return render(request, 'thresh-holds.html', context)
   