from unicodedata import name
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('search/', views.search, name='search'),
    path('random/', views.random, name='random'),
    path('entry/', views.new_entry, name='new_entry'),
    path('edit/<str:title>/', views.edit, name='edit'),
    path('<str:title>/', views.entries, name='entries'),
]
