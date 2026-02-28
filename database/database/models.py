from django.db import models
import uuid


class Shop(models.Model):
    shop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    shop_name = models.CharField(max_length=1024)
    # shop_address = models.CharField(max_length=1024)

    shop_stock = models.IntegerField(default=0)
    # shop_sales = models.IntegerField(default=0)

class Product(models.Model):
    product_sku = models.CharField(max_length=50)
    product_name = models.CharField(max_length=250)
    product_variant = models.CharField(max_length=250)

    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"

    SIZE_CHOICES = {
        XS: "Extra Small",
        S: "Small",
        M: "Medium",
        L: "Large",
        XL: "Extra Large"
    }

class Sales_Data(models.Model):
    shop = Shop()
    product = Product()

    variant_sku = product.id 
    pos_location_name = shop.shop_name
    net_items_sold = models.IntegerField(default=0)
    gross_sales = models.IntegerField(default=0)
    discounts = models.FloatField(default=0.0)
    returns = models.IntegerField(default=0)
    net_sales = models.FloatField(default=0.0)
    taxes = models.FloatField(default=0.0)
    total = sales = models.FloatField(default=0.0)
