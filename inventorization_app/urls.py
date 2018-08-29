from django.contrib import admin
from django.urls import re_path
from .views import send_mail_to_admin, ProductCreateView, ProductListView, ProductRetrieveUpdateDestroyView, ProductListPDFView, AcceptOwnerView, DenyOwnerView
from rest_framework.routers import DefaultRouter

app_name = 'inventorization_urls'

#owner_url_path = 'owner_accept/(?P<user>[0-9]+)/(?P<pk>[0-9]+)$'
#router = DefaultRouter()
#router.register(r'owner_url_path, CheckOwnerView', name="owner_accept")

urlpatterns = [
   re_path(r'^$', ProductListView.as_view(), name='list'), 
   re_path(r'^create/$', ProductCreateView.as_view(), name='create'),
   re_path(r'^(?P<pk>\d+)/$', ProductRetrieveUpdateDestroyView.as_view(), name='detail'),  #re_path(r'^(?P<id>\d+)/edit/$', "products.views.products_update", name='update'),    # re_path(r'^(?P<id>\d+)/delete/$', "products.views.products_delete", name='delete'),
   re_path(r'^(?P<pk>\d+)/send$', send_mail_to_admin, name='detail'),
   # re_path(r'^(?P<id>\d+)/borrow/$', "products.views.products_borrow", name='borrow'),
   re_path(r'^generate_pdf/$', ProductListPDFView.as_view(), name='generate_pdf'),
   re_path(r'^owner_accept/(?P<user>[0-9]+)/(?P<pk>[0-9]+)$', AcceptOwnerView.as_view({'get': 'retrive'}), name="owner_accept"),
   re_path(r'^owner_deny/(?P<user>[0-9]+)/(?P<pk>[0-9]+)$', DenyOwnerView.as_view({'get': 'retrive'}), name="owner_deny"),   
]