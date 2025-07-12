from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrowsableLoginView, ProductViewSet, ReviewViewSet, RegisterUserAPIView
from rest_framework_nested.routers import NestedDefaultRouter

# Base router
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')

# Nested router for reviews
product_router = NestedDefaultRouter(router, r'products', lookup='product')
product_router.register(r'reviews', ReviewViewSet, basename='product-reviews')

urlpatterns = [
    path('', include(router.urls)),              # /api/products/
    path('', include(product_router.urls)),      # /api/products/<id>/reviews/
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', BrowsableLoginView.as_view(), name='login'), 
    
]
