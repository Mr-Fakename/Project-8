import requests
from django.core.management.base import BaseCommand
from website.models import Product, Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        api = OpenFoodFactsAPI()
        api.get_data()
        api.cleaner()
        api.make_readable()
        api.get_categories()
        print("Database completed!")


class OpenFoodFactsAPI:
    def __init__(self):
        self.raw_data = None
        self.cleaned_data = []

        self.categories = []

    def get_data(self):
        url = "https://world.openfoodfacts.org/language/french?"
        headers = {"User-Agent": "PurBeurre/OpenClassRooms - Python/Windows - Version 2.0"}
        payload = {"action": "process",
                   "sort_by": "unique_scans_n",
                   "page_size": 1000,
                   "json": 'true',
                   "fields": "brands,stores,nutriscore_grade,"
                             "categories,product_name_fr,code,image_url,categories_lc"
                   }

        r = requests.get(url, params=payload, headers=headers)
        self.raw_data = r.json()

    def cleaner(self):
        """ Takes json data that was extracted from the OpenFoodFacts API with the 'get_data()' function
            Dict comprehension checks if some values are missing. If it is the case, the associated key
            is deleted.
            The function then loops over all products and stores those containing all the keys we want to use,
            ensuring we only work with complete data.
        """

        self.raw_data = [{key: value for key, value in product.items() if value} for product in
                         self.raw_data["products"]]

        tags = ['brands', 'categories', 'code', 'nutriscore_grade', 'product_name_fr', 'stores', 'image_url',
                'categories_lc']

        for product in self.raw_data:
            try:
                if all(key in product for key in tags):
                    if product['categories_lc'] == 'fr':
                        self.cleaned_data.append(product)
            except Exception as e:
                continue

    def make_readable(self):
        """ Performs string formatting: proper capitalization, removal of unnecessary spaces,
            makes lists from keys with several values.
        """

        for product in self.cleaned_data:
            product["product_name_fr"] = product['product_name_fr'].title()
            product["nutriscore_grade"] = product["nutriscore_grade"].upper()

            product["brands"] = str(list(map(str.strip, product["brands"].title().split(','))))
            product["categories"] = ", ".join(map(str.strip, product["categories"].split(',')))
            product["stores"] = str(list(map(str.strip, product["stores"].title().split(','))))

    def get_categories(self):
        for product in self.cleaned_data:
            self.categories.append(product['categories'].split(", ")[:1])

        self.categories = [category for sublist in self.categories for category in sublist]
        self.categories = sorted(self.categories, key=self.categories.count, reverse=True)

        # The 3 following lines delete duplicate categories and keep them in order
        seen = set()
        seen_add = seen.add
        self.categories = [x for x in self.categories if not (x in seen or seen_add(x))][:15]


def create_categories(api_data):
    for category in api_data.categories:
        try:
            new_category = Category(
                name=category
            )
            new_category.save()
            print(f'Added "{category}" to the database')
        except Exception as e:
            continue


def create_products(api_data):
    for product in api_data.cleaned_data:
        try:
            new_product = Product(
                name=product['product_name_fr'],
                brands=product['brands'],
                code=product['code'],
                nutriscore=product['nutriscore_grade'],
                stores=product['stores'],
                picture=product['image_url']
            )
            new_product.save()

            product_category_query = "".join(product['categories'].split(", ")[0])
            product_category = Category.objects.filter(name__icontains=product_category_query).first()
            if product_category:
                product_category.products.add(new_product)
                product_category.save()
                print(f'Added "{product["product_name_fr"]}" to the database')
            else:
                new_product.delete()
                print(f'No category found for {product["product_name_fr"]}')
        except KeyError:
            continue
