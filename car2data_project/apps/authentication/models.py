from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string

class UserSubscription(models.Model):
    """Modelo para manejar las suscripciones de usuario"""
    
    PLAN_CHOICES = [
        ('starter', 'Starter'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='starter')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Control de documentos
    documents_used = models.IntegerField(default=0)
    
    # Información de pago
    payment_status = models.CharField(max_length=20, default='completed')  # completed por defecto para plan free
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_plan_display()}"
    
    def get_plan_price(self):
        """Retorna el precio del plan"""
        prices = {
            'starter': 0,
            'pro': 19,
            'enterprise': 0,  # A medida
        }
        return prices.get(self.plan, 0)
    
    def is_free_plan(self):
        """Verifica si es plan gratuito"""
        return self.plan == 'starter'
    
    def get_documents_limit(self):
        """Retorna el límite de documentos según el plan"""
        limits = {
            'starter': 3,
            'pro': 100,
            'enterprise': 999999,  # Ilimitado
        }
        return limits.get(self.plan, 3)
    
    def can_generate_document(self):
        """Verifica si puede generar más documentos"""
        return self.documents_used < self.get_documents_limit()
    
    def increment_documents(self):
        """Incrementa el contador de documentos usados"""
        self.documents_used += 1
        self.save()
    
    def get_remaining_documents(self):
        """Retorna documentos restantes"""
        return max(0, self.get_documents_limit() - self.documents_used)

class VerificationCode(models.Model):
    """Modelo para almacenar códigos de verificación de email y recuperación de contraseña"""
    
    CODE_TYPE_CHOICES = [
        ('email_verification', 'Verificación de Email'),
        ('password_reset', 'Recuperación de Contraseña'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_codes')
    code = models.CharField(max_length=6)
    code_type = models.CharField(max_length=20, choices=CODE_TYPE_CHOICES)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.email} - {self.code_type} - {self.code}"
    
    @staticmethod
    def generate_code():
        """Genera un código de 6 dígitos"""
        return ''.join(random.choices(string.digits, k=6))
    
    def is_valid(self):
        """Verifica si el código es válido (no usado y no expirado)"""
        return not self.is_used and timezone.now() < self.expires_at
    
    def mark_as_used(self):
        """Marca el código como usado"""
        self.is_used = True
        self.save()
