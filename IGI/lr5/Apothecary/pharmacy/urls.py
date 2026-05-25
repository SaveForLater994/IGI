from django.urls import path
from django.urls import include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('faq/', views.faq, name='faq'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy/', views.privacy, name='privacy'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/add/', views.add_review, name='add_review'),
    path('promocodes/', views.promocodes, name='promocodes'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:medication_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:cart_item_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/apply-promo/', views.apply_promo, name='apply_promo'),
    path('medications/', views.medication_list, name='medication_list'),
    path('faq/', views.faq, name='faq'),
    path('checkout/', views.checkout, name='checkout'),
    path('sales-chart/', views.sales_chart, name='sales_chart'),
    path('create-superuser/', views.create_superuser, name='create_superuser'),
]