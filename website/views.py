from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Product
from django.views.generic import ListView


def index(request):
    return render(request, 'website/index.html')


class ProductsSearchListView(ListView):
    model = Product
    template_name = 'website/products.html'
    context_object_name = 'products'
    paginate_by = 21

    def get_queryset(self):
        query = self.request.GET.get('query')
        products = Product.objects.filter(name__icontains=query)
        if not products:
            products = get_list_or_404(Product, generic_name__icontains=query)
        return products

    def get_context_data(self, *args, **kwargs):
        context = super(ProductsSearchListView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('query')
        context['title'] = "Résultats pour la requête %s" % query
        return context
