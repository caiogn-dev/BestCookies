from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('produto/<int:pk>/', ProductDetailView.as_view(), name='produto_detalhe'),
    path('adicionar/<int:pk>/', AddToCartView.as_view(), name='add_carrinho'),
    path('carrinho/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
