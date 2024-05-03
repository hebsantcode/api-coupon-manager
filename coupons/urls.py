from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='coupon_create'),
    path('delete/', views.delete, name='delete_coupon'),
    path('update/', views.update, name='update_coupon'),
    path('all/', views.get_coupons, name='get_coupons'),
    path('fetch-members/', views.mailchimp_total_members, name='mailchimp_total_members'),
    path('pagination/', views.maichimp_pagination, name='mailchimp_pagination'),
    path('apply/', views.is_valid_for_coupons, name='is_valid_for_coupons'),
]