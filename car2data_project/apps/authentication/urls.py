from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('settings/', views.UserSettingsView.as_view(), name='settings'),
    # Email verification
    path('verify-email/', views.VerifyEmailPromptView.as_view(), name='verify_email_prompt'),
    path('verify-email/submit/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('verify-email/resend/', views.ResendVerificationCodeView.as_view(), name='resend_verification'),
    # Password reset
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('verify-reset-code/', views.VerifyResetCodeView.as_view(), name='verify_reset_code'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    # Checkout
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]