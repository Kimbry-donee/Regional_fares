from django.urls import path
from . import views


app_name = 'Nauli'
urlpatterns = [
  path('ping/', views.mailchimp_ping_view),
  path('',views.searchFare, name='searchFare'),
  path('subscribe/', views.subscribe_view, name='subscribe'),
  path('success/', views.subscribe_success_view, name='subscribe-success'),
  path('fail/', views.subscribe_fail_view, name='subscribe-fail'),
  path('unsubscribe/', views.unsubscribe_view, name='unsubscribe'),
  path('unsubscribe/success/', views.unsubscribe_success_view, name='unsubscribe-success'),
  path('unsubscribe/fail/', views.unsubscribe_fail_view, name='unsubscribe-fail'),
]