from django.db import models


class Price(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = ('product', 'store')

    def __str__(self):
        return f'{self.store}, {self.price}'


class Product(models.Model):
    upc = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=512, default='')
    target_url = models.URLField(max_length=512, unique=True, null=True)
    frys_url = models.URLField(max_length=512, unique=True, null=True)
    bestbuy_url = models.URLField(max_length=512, unique=True, null=True)

    def __str__(self):
        return f'Product(upc={self.upc}, name={self.name})'


class Store(models.Model):
    name = models.CharField(max_length=128, unique=True)
    url = models.URLField(max_length=512, unique=True)

    def __str__(self):
        return f'Store(name={self.name})'

