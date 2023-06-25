from django.urls import path
from . import views

urlpatterns = [
    path('mdbstore/', views.mdbstore, name='mdbstore'),
]