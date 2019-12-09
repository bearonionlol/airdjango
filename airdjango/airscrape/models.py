from django.db import models


class Price(models.Model):
    stores_and_prices = models.CharField(max_length=200)
    cheapest_price = models.CharField(max_length=200)

    def __str__(self):
        # return 'asdf'
        return self.stores_and_prices, self.cheapest_price
