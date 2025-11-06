from django.contrib import admin
from .models import VerificationCode, UserSubscription

@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'code_type', 'code', 'is_used', 'created_at', 'expires_at')
    list_filter = ('code_type', 'is_used', 'created_at')
    search_fields = ('user__username', 'email', 'code')
    readonly_fields = ('created_at',)
    
@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'payment_status', 'is_active', 'created_at', 'updated_at')
    list_filter = ('plan', 'payment_status', 'is_active', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user', 'plan', 'is_active')
        }),
        ('Información de Pago', {
            'fields': ('payment_status', 'stripe_customer_id', 'stripe_subscription_id')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at')
        }),
    )
