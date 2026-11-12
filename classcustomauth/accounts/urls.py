from django.urls import path 
from accounts.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_change'),
    path('forgot-password/', CustomPasswordResetView.as_view(), name='password_forgot'),
    path('password_forgot_done/<uidb64>/<token>/', PasswordResetDoneView.as_view(), name='password_reset_done'),


]  