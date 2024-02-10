from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('product/<int:id>', views.detail, name="detail"),
    path('success/<int:id>', views.payment_success_view, name="success"),
]
