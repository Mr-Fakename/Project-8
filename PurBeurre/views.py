from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def product_details(request):
    return render(request, 'product.html')
