import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Product(models.Model):
    name = models.CharField("Nom du produit", max_length=128, default=None)
    brands = models.CharField("Marque du produit", max_length=128, default=None)
    code = models.IntegerField(default=None)
    nutriscore = models.CharField("Nutriscore du produit", max_length=1, default=None)
    stores = models.CharField("Magasins stockant le produit", max_length=128, default=None)
    picture = models.URLField(default=None)
    users = models.ManyToManyField(
        User,
        through="Favourite",
        through_fields=('replacement_product', 'user')
    )

    def __str__(self):
        return self.name

    @property
    def url(self):
        return "https://fr.openfoodfacts.org/produit/" + str(self.code)

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'


class Category(models.Model):
    name = models.CharField(max_length=128)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    replacement_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_favourited = models.DateTimeField(default=timezone.now)
    replaced_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='replaced_product'
    )

    def __str__(self):
        return self.replacement_product

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})

    def was_favourited_recently(self):
        return self.date_favourited >= timezone.now() - datetime.timedelta(days=1)

    class Meta:
        verbose_name = 'Favoris'
        verbose_name_plural = 'Favoris'
