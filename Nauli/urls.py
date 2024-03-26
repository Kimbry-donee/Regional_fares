from django.urls import path
from . import views


app_name = 'Nauli'
urlpatterns = [
  path('',views.searchFare, name='searchFare'),
]