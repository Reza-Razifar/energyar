from django.urls import path
from . import views

urlpatterns = [
    path('', views.Orders.as_view(), name='orders'),
    path('<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
]
