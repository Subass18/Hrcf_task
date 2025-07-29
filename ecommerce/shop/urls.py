from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('carts', CartViewSet)
router.register('cart-items', CartItemViewSet,basename='cartitem')
router.register('orders', OrderViewSet,basename='order')
router.register(r'products', ProductAdminViewSet, basename='admin-product')
router.register(r'orders', AdminOrderViewSet,basename='admin-orders')


urlpatterns = [
    path('', include(router.urls)),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('register/', register_view, name='register'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('order/place/', PlaceOrderView.as_view(), name='place-order'),
    path('admin/orders/', OrderListAdminView.as_view(), name='admin-orders'),
    path("orders/", UserOrdersView.as_view(), name="user-orders"),
    path("place-order/", place_order, name="place-order"),
    path("admin-summary/", admin_summary, name="admin-summary"),
    path("my-orders/", my_orders, name="my-orders"),



]

