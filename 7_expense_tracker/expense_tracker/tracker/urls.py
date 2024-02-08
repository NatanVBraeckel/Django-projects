from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('edit/<int:id>/', views.edit, name="edit"),
]
