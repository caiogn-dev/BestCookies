from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from loja.models import Product, Category, Order, Customer, CartItem

class ProductAPITests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="TestCat")
        self.product = Product.objects.create(name="Cookie Teste", price=10, available=True, category=self.category)

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

class CategoryAPITests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="TestCat")

    def test_list_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

class MeViewAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.customer = Customer.objects.create(user=self.user, address="Rua Teste", cep="12345-678")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_me_view_authenticated(self):
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['address'], "Rua Teste")

    def test_me_view_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class OrderAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="orderuser", password="orderpass")
        self.customer = Customer.objects.create(user=self.user, address="Rua Teste", cep="12345-678")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_orders(self):
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CustomerAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="custuser", password="custpass")
        self.customer = Customer.objects.create(user=self.user, address="Rua Teste", cep="12345-678")

    def test_list_customers(self):
        url = reverse('customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CartItemAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cartuser", password="cartpass")
        self.customer = Customer.objects.create(user=self.user, address="Rua Teste", cep="12345-678")
        self.category = Category.objects.create(name="TestCat")
        self.product = Product.objects.create(name="Cookie Teste", price=10, available=True, category=self.category)
        self.cartitem = CartItem.objects.create(customer=self.customer, product=self.product, quantity=2)

    def test_list_cartitems(self):
        url = reverse('cartitem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
