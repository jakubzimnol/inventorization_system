from django.contrib import admin
from django.urls import re_path
# from .views import ProductListPDFView
from .views import ProductViewSet
from rest_framework.routers import DefaultRouter

app_name = 'inventorization_urls'
router = DefaultRouter()
router.register(r'', ProductViewSet, base_name='products')
urlpatterns = [
#    re_path(r'^generate_pdf/$', ProductListPDFView.as_view(), name='generate_pdf'),
 ]
urlpatterns += router.urls
