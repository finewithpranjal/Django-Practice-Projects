from django.urls import path
from seller.views import *
urlpatterns = [

 path('dashboard/', SellerDashBoardView.as_view(), name='seller_dashboard'),
 path('password_change/', SellerPasswordChangeView.as_view(), name='seller_password_change'),
    
]
