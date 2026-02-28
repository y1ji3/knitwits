from django.db import models
import uuid

class Sizes(models.TextChoices):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"

    SIZE_STRINGS = {
        XS: "X-Small",
        S: "Small",
        M: "Medium",
        L: "Large",
        XL: "X-Large"
    }

class Shop(models.Model):
    shop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    # shop_address = models.CharField(max_length=1024)

    def __str__(self):
        return f'{self.shop_id}: {self.name}'
    

class Product(models.Model):
    sku = models.CharField(max_length=50)
    name = models.CharField(max_length=250)
    variant = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.sku}: {self.name} -- {self.variant}'

class ShopInventory(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="inventory")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} at {self.shop.name}"

    class Meta:
        unique_together = ('shop', 'product')  


# class Sales_Data(models.Model):
#     shop = Shop()
#     product = Product()

#     variant_sku = product.id 
#     pos_location_name = shop.shop_name
#     net_items_sold = models.IntegerField(default=0)
#     gross_sales = models.IntegerField(default=0)
#     discounts = models.FloatField(default=0.0)
#     returns = models.IntegerField(default=0)
#     net_sales = models.FloatField(default=0.0)
#     taxes = models.FloatField(default=0.0)
#     total = sales = models.FloatField(default=0.0)
