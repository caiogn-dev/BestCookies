from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import Product, CartItem, Customer, Order
from .forms import CustomUserCreationForm, EmailAuthenticationForm

# Lista de produtos
class HomeView(ListView):
    model = Product
    template_name = 'loja/home.html'
    context_object_name = 'produtos'
    queryset = Product.objects.filter(available=True)

# Detalhes do produto
class ProductDetailView(DetailView):
    model = Product
    template_name = 'loja/product_detail.html'
    context_object_name = 'produto'

# Adicionar ao carrinho
class AddToCartView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, pk):
        produto = get_object_or_404(Product, pk=pk)
        customer, _ = Customer.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(customer=customer, product=produto)
        item.quantity += 1
        item.save()
        return redirect('cart')

# Ver carrinho
class CartView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'loja/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer, _ = Customer.objects.get_or_create(user=self.request.user)
        items = CartItem.objects.filter(customer=customer)
        total = sum(item.get_total_price() for item in items)
        context['items'] = items
        context['total'] = total
        return context

# Checkout
class CheckoutView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'loja/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer, _ = Customer.objects.get_or_create(user=self.request.user)
        items = CartItem.objects.filter(customer=customer)
        order = Order.objects.create(customer=customer)
        order.items.set(items)
        order.save()
        items.delete()
        context['order'] = order
        return context

# Registro de usuário
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')

# Login de usuário com e-mail
class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    authentication_form = EmailAuthenticationForm
    next_page = reverse_lazy('home')

# Logout de usuário
class CustomLogoutView(LogoutView):
    template_name = 'auth/logged_out.html'
    next_page = reverse_lazy('home')