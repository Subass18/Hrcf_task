from rest_framework import serializers
from .models import Category, Product, Cart, CartItem, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    product = ProductSerializer(read_only=True)


    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

