from django.urls import path

from . import views

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.search, name='search'),
]
