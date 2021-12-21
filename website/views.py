from django.shortcuts import render, get_list_or_404
from .models import Product


def index(request):
    return render(request, 'website/index.html')


def search(request):
    query = request.GET.get('query')
    if not query:
        products = Product.objects.all()
    else:
        # title contains the query is and query is not sensitive to case.
        products = Product.objects.filter(name__icontains=query)
    if not products.exists():
        products = Product.objects.filter(generic_name__icontains=query)
    title = "Résultats pour la requête %s"%query
    context = {
        'products': products,
        'title': title
    }
    return render(request, 'website/products.html', context)
