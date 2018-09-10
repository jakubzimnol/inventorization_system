from rest_framework.routers import DefaultRouter

from .views import ProductViewSet

app_name = 'inventorization_urls'
router = DefaultRouter()
router.register(r'', ProductViewSet, base_name='products')
urlpatterns = []
urlpatterns += router.urls
