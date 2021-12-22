from django.urls import path
from .views import ProductsSearchListView
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    # path('products/', views.search, name='search'),
    path('search', ProductsSearchListView.as_view(), name="search"),
]
