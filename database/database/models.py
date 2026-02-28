from django.db import models
import uuid

class Sizes(models.TextChoices):
    XS = "XS", "X-Small"
    S = "S", "Small"
    M = "M", "Medium"
    L = "L", "Large"
    XL = "XL", "X-Large"

class Product(models.Model):
    sku = models.CharField(max_length=50)
    name = models.CharField(max_length=250)
    variant = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.sku}: {self.name} -- {self.variant}'

class Shop(models.Model):
    class Tier(models.TextChoices):
        # A = "A", "A Tier"
        # B = "B", "B Tier"
        pass

    shop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    # tier = models.CharField(max_length=1, choices=Tier.choices, default=Tier.A)

    def __str__(self):
        return f'{self.shop_id}: {self.name}'

class TierThreshold(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='thresholds')
    xs_thresh = models.IntegerField(default=0)
    s_thresh = models.IntegerField(default=0)
    m_thresh = models.IntegerField(default=0)
    l_thresh = models.IntegerField(default=0)
    xl_thresh = models.IntegerField(default=0)

class DistributionCenter(models.Model):
    name = models.CharField(max_length=1024)
    allocation = models.IntegerField(default=0)  
    shops = models.ManyToManyField(Shop, related_name='distribution_centers', blank=True)

    def __str__(self):
        return self.name

class DCInventory(models.Model):
    dc = models.ForeignKey(DistributionCenter, on_delete=models.CASCADE, related_name='inventory')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='dc_inventory')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} at {self.dc.name}"

    class Meta:
        unique_together = ('dc', 'product')

class ShopInventory(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="inventory")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} at {self.shop.name}"

    class Meta:
        unique_together = ('shop', 'product')  

class Category(models.Model):
    name = models.CharField(max_length=1024)
    par_level = models.IntegerField(default=0)
    products = models.ManyToManyField(Product, related_name='categories', blank=True)

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
