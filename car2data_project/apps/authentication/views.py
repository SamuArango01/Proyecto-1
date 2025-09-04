from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(DjangoLoginView):
    template_name = 'authentication/login.html'
    
    def get_success_url(self):
        return reverse_lazy('documents:dashboard')

class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('authentication:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cuenta creada exitosamente. Por favor inicia sesión.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear la cuenta. Por favor verifica los datos.')
        return super().form_invalid(form)

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('documents:dashboard')
        return super().get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('authentication:login')