from rest_framework import viewsets
from loja.models import Product, Category, Order, Customer, CartItem
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, CustomerSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .serializers import CustomerSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({"detail": "Cliente não encontrado."}, status=404)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        customer = Customer.objects.get(user=self.request.user)
        serializer.save(customer=customer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Só diminui a quantidade se for maior que 1, senão deleta
        if instance.quantity > 1:
            instance.quantity -= 1
            instance.save()
            return Response({'detail': 'Quantidade reduzida', 'quantity': instance.quantity})
        else:
            return super().destroy(request, *args, **kwargs)
