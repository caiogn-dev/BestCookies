from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import Product, CartItem, Customer, Order
from .forms import CustomUserCreationForm, EmailAuthenticationForm
from django.http import HttpResponse, Http404
from django.conf import settings
import os

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
    def post(self, request, pk):
        print('DEBUG: AddToCartView chamada para produto', pk, 'por', request.user)
        produto = get_object_or_404(Product, pk=pk)
        customer, _ = Customer.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(customer=customer, product=produto)
        if not created:
            item.quantity += 1
            item.save()
        # Se foi criado agora, já começa com 1
        return redirect('cart')
    def get(self, request, pk):
        return redirect('cart')

# Remover do carrinho
class RemoveFromCartView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, customer__user=request.user)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
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
        context['items'] = items
        context['total'] = sum(item.get_total_price() for item in items)
        return context

    def post(self, request, *args, **kwargs):
        customer, _ = Customer.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(customer=customer)
        if not items.exists():
            return render(request, 'loja/checkout.html', {'items': items, 'total': 0, 'erro': 'Seu carrinho está vazio.'})
        # Atualiza endereço se editado
        endereco = request.POST.get('endereco')
        if endereco and endereco != customer.address:
            customer.address = endereco
            customer.save()
        order = Order.objects.create(customer=customer)
        from .models import OrderItem
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        items.delete()
        # Se for pedido via WhatsApp, monta a URL e redireciona
        if request.POST.get('whatsapp'):
            pagamento = request.POST.get('pagamento')
            nome = request.user.get_full_name() or request.user.username
            pedido = '\n'.join([
                f"{oi.quantity}x {oi.product.name} - R$ {oi.get_total_price():.2f}" for oi in order.order_items.all()
            ])
            total = order.get_total()
            msg = (
                f"Olá! Quero finalizar meu pedido:\n{pedido}\nTotal: R$ {total:.2f}\n"
                f"Método de pagamento: {pagamento}\nNome: {nome}\nEndereço: {customer.address}"
            )
            numero = '5563920014688'
            whatsapp_url = f"https://wa.me/{numero}?text=" + msg.replace(' ', '%20').replace('\n', '%0A')
            return render(request, 'loja/checkout.html', {'order': order, 'finalizado': True, 'whatsapp_url': whatsapp_url})
        return render(request, 'loja/checkout.html', {'order': order, 'finalizado': True})

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


class MediaListView(View):
    def get(self, request, path=''):
        abs_path = os.path.join(settings.MEDIA_ROOT, path)
        if not os.path.exists(abs_path):
            # Se for o diretório raiz e não existir, cria para evitar erro
            if path == '' and not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                files = []
            else:
                raise Http404("Arquivo ou diretório não encontrado.")
        else:
            if os.path.isfile(abs_path):
                # Serve o arquivo de mídia
                from django.http import FileResponse
                import mimetypes
                mime_type, _ = mimetypes.guess_type(abs_path)
                response = FileResponse(open(abs_path, 'rb'), content_type=mime_type or 'application/octet-stream')
                return response
            files = os.listdir(abs_path)
        if not files:
            return HttpResponse(f'<h2>Sem arquivos em /imagens/{path}</h2>')
        links = []
        for f in files:
            url = request.path.rstrip('/') + '/' + f
            links.append(f'<li><a href="{url}">{f}</a></li>')
        return HttpResponse(f'<h2>Arquivos em /imagens/{path}</h2><ul>{''.join(links)}</ul>')

class OrderHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'loja/order_history.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        context['orders'] = Order.objects.filter(customer=customer).order_by('-ordered_at')
        return context
