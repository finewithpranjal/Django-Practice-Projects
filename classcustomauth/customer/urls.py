from django.urls import path
from customer.views import *
urlpatterns = [

 path('dashboard/', CustomerDashBoardView.as_view(), name='customer_dashboard'),
 path('password_change/', CustomerPasswordChangeView.as_view(), name='password_change'),
    
]