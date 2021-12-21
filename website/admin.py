from django.contrib import admin
from .models import Product, Category, Favourite


admin.site.register([Product, Category, Favourite])
