from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

# Formulário de criação de usuário com e-mail
class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(
        required=True, label="Nome",
        widget=forms.TextInput(attrs={
            "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50 py-2 px-3 mb-2"
        })
    )
    email = forms.EmailField(
        required=True, label="E-mail",
        widget=forms.EmailInput(attrs={
            "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50 py-2 px-3 mb-2"
        })
    )
    address = forms.CharField(
        required=True, label="Endereço",
        widget=forms.Textarea(attrs={
            "rows": 2,
            "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50 py-2 px-3 mb-2"
        })
    )
    cep = forms.CharField(
        required=True, label="CEP", max_length=9,
        widget=forms.TextInput(attrs={
            "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50 py-2 px-3 mb-2"
        })
    )

    class Meta:
        model = User
        fields = ("name", "email", "address", "cep", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["name"]
        if commit:
            user.save()
            # Cria o Customer com endereço
            from .models import Customer
            Customer.objects.create(user=user, address=self.cleaned_data["address"], cep=self.cleaned_data["cep"])
        return user

# Formulário de login via e-mail
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label=_("E-mail"), widget=forms.EmailInput(attrs={"autofocus": True}))

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            raise forms.ValidationError("E-mail não encontrado.")

        self.user_cache = authenticate(self.request, username=username, password=password)
        if self.user_cache is None:
            raise self.get_invalid_login_error()
        self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data