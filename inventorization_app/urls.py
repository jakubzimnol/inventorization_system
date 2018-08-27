from django.contrib import admin
from django.urls import re_path
from .views import products_generate_pdf
app_name = 'inventorization_urls'
urlpatterns = [
   # re_path(r'^/$', "products.product_list", name='list'),
   # re_path(r'^create/$', "products.views.products_create", name='create'),
   # re_path(r'^(?P<id>\d+)/$', "products.views.products_detail", name='detail'),
   # re_path(r'^(?P<id>\d+)/edit/$', "products.views.products_update", name='update'),
   # re_path(r'^(?P<id>\d+)/delete/$', "products.views.products_delete", name='delete'),
   # re_path(r'^(?P<id>\d+)/borrow/$', "products.views.products_borrow", name='borrow'),
    re_path(r'^generate_pdf/$', products_generate_pdf, name='generate_pdf'),
]