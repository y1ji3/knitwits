import json
from decimal import Decimal
from django.db import models


class POSSalesByProductVariant(models.Model):
    product_title = models.CharField(max_length=255)
    product_variant_title = models.CharField(max_length=255)
    product_variant_sku = models.CharField(max_length=100)
    pos_location_name = models.CharField(max_length=255)
    net_items_sold = models.IntegerField()
    gross_sales = models.DecimalField(max_digits=10, decimal_places=2)
    discounts = models.DecimalField(max_digits=10, decimal_places=2)
    returns = models.DecimalField(max_digits=10, decimal_places=2)
    net_sales = models.DecimalField(max_digits=10, decimal_places=2)
    taxes = models.DecimalField(max_digits=10, decimal_places=2)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "POS Sales by Product Variant"
        verbose_name_plural = "POS Sales by Product Variant"

    def __str__(self):
        return f"{self.product_title} - {self.product_variant_title} ({self.pos_location_name})"

    @classmethod
    def from_dict(cls, data: dict) -> "POSSalesByProductVariant":
        """Create (but don't save) a model instance from a raw JSON dict."""
        return cls(
            product_title=data["product_title"],
            product_variant_title=data["product_variant_title"],
            product_variant_sku=data["product_variant_sku"],
            pos_location_name=data["pos_location_name"],
            net_items_sold=int(data["net_items_sold"]),
            gross_sales=Decimal(str(data["gross_sales"])),
            discounts=Decimal(str(data["discounts"])),
            returns=Decimal(str(data["returns"])),
            net_sales=Decimal(str(data["net_sales"])),
            taxes=Decimal(str(data["taxes"])),
            total_sales=Decimal(str(data["total_sales"])),
        )

    @classmethod
    def import_from_file(cls, file_path: str, clear_existing: bool = False) -> dict:
        """
        Import records from a JSON or JSONL file.

        Supports:
          - .jsonl  — one JSON object per line
          - .json   — either a single object or a list of objects

        Args:
            file_path:      Path to the JSON / JSONL file.
            clear_existing: If True, deletes all existing rows before importing.

        Returns:
            A dict with keys 'created', 'skipped', and 'errors'.
        """
        created = 0
        skipped = 0
        errors = []

        if clear_existing:
            cls.objects.all().delete()

        with open(file_path, "r", encoding="utf-8") as f:
            if file_path.endswith(".jsonl"):
                rows = (json.loads(line) for line in f if line.strip())
            else:
                raw = json.load(f)
                rows = raw if isinstance(raw, list) else [raw]

            instances = []
            for i, row in enumerate(rows, start=1):
                try:
                    instances.append(cls.from_dict(row))
                except (KeyError, ValueError) as exc:
                    errors.append({"line": i, "error": str(exc), "data": row})
                    skipped += 1

        # Bulk-insert for efficiency
        cls.objects.bulk_create(instances)
        created = len(instances)

        return {"created": created, "skipped": skipped, "errors": errors}
