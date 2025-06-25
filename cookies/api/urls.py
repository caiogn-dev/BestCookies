from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'cart', CartItemViewSet)

urlpatterns = router.urls