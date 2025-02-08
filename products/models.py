from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    image = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    installment_options = models.CharField(max_length=100, blank=True)
    delivery_type = models.CharField(max_length=50, choices=[('Full', 'Full'), ('Normal', 'Normal')])
    free_shipping = models.BooleanField(default=False)

    def __str__(self):
        return self.name