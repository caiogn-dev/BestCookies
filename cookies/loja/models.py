# cookies/loja/models.py
# Modelos para a loja de cookies
from django.db import models
from django.contrib.auth.models import User

# Categoria dos produtos
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

# Produto (Cookie)
class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Cliente (vinculado ao User)
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    cep = models.CharField(max_length=9, blank=True)

    def __str__(self):
        return self.user.username

# Item do Carrinho
class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.product.price * self.quantity

# Item do Pedido (snapshot do produto no momento do pedido)
class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)  # preço no momento do pedido

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Pedido #{self.order.pk})"

    def get_total_price(self):
        return self.price * self.quantity

# Pedido
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='Pendente')

    def __str__(self):
        return f"Pedido #{self.pk} por {self.customer.user.username}"

    def get_total(self):
        return sum(item.get_total_price() for item in self.order_items.all())
