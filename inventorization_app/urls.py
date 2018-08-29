from django.contrib import admin
from django.urls import re_path
from .views import send_mail_to_admin, ProductCreateView, ProductListView, ProductRetrieveUpdateDestroyView, ProductListPDFView, CheckAcessView
app_name = 'inventorization_urls'
urlpatterns = [
   re_path(r'^$', ProductListView.as_view(), name='list'), 
   re_path(r'^create/$', ProductCreateView.as_view(), name='create'),
   re_path(r'^(?P<pk>\d+)/$', ProductRetrieveUpdateDestroyView.as_view(), name='detail'),  #re_path(r'^(?P<id>\d+)/edit/$', "products.views.products_update", name='update'),    # re_path(r'^(?P<id>\d+)/delete/$', "products.views.products_delete", name='delete'),
   re_path(r'^(?P<pk>\d+)/send$', send_mail_to_admin, name='detail'),
   # re_path(r'^(?P<id>\d+)/borrow/$', "products.views.products_borrow", name='borrow'),
   re_path(r'^generate_pdf/$', ProductListPDFView.as_view(), name='generate_pdf'),
   re_path(r'^allow_access/(?P<pk>[0-9]+)$', CheckAcessView.as_view({'get': 'list'}), name="grant_access"),
   re_path(r'^deny_access/(?P<pk>[0-9]+)$', CheckAcessView.as_view({'get': 'retrive'}), name="deny_access"),   
]