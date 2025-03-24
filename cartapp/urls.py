from django.urls import path
from . import views

app_name = 'cartapp'

urlpatterns = [
    path('add/<uuid:ticket_id>', views.CartAdd, name='cart_add'),
    path('', views.cart_detail, name='cart_detail'),
]