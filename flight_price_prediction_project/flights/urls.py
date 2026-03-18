from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('search/', views.flights_search_page, name='flights_search'),
]