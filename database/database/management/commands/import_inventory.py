import csv
from django.core.management.base import BaseCommand
from database.models import Shop, Product, ShopInventory

LOCATION_COLUMNS = [
    '9783 South 600 West', 'Main Warehouse Receiving', 'Fashion Place',
    'The Shops at South Towne', 'University Place', 'City Creek',
    'Station Park', 'Newgate Mall', 'Southgate Mall', 'Grand Teton Mall',
    'Magic Valley Mall', 'Red Cliffs', 'Damages', 'Mountain View Village',
    'Meridian', 'SanTan Village', 'Warehouse Sale', 'Logan'
]

class Command(BaseCommand):
    help = 'Import inventory from CSV'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                # Get or create the product
                product, _ = Product.objects.get_or_create(
                    sku=r['SKU'],
                    defaults={
                        'name': r['Title'],
                        'variant': f"{r['Option1 Value']} / {r['Option2 Value']}".strip(' /'),
                    }
                )

                for location in LOCATION_COLUMNS:
                    stock = int(r.get(location, '0') or '0')

                    # Get or create the shop
                    shop, _ = Shop.objects.get_or_create(name=location)

                    # Create or update inventory
                    ShopInventory.objects.update_or_create(
                        shop=shop,
                        product=product,
                        defaults={'stock': stock}
                    )

        self.stdout.write(self.style.SUCCESS('Inventory imported successfully.'))