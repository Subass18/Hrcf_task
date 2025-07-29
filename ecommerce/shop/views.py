from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *
from .permissions import IsAdminOrOwner
from .permissions import IsAdminOrReadOnly
from .views import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

User = get_user_model()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def get_queryset(self):
        return Product.objects.all()

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all() 
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(cart__user=user) 
    
    @action(detail=False, methods=['post'])
    def place_order(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart or not cart.cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(cart=cart, status='Pending')

        for item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        cart.cart_items.all()
        return Response({"message": "Order placed successfully"}, status=status.HTTP_201_CREATED)


    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(cart=user.cart)

@api_view(['POST'])
def register_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response({"error": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(email=email, password=password)
    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        cart, created = Cart.objects.get_or_create(
            user=request.user,
            product_id=product_id,
            defaults={"quantity": quantity}
        )
        if not created:
            cart.quantity += quantity
            cart.save()

        return Response({"message": "Added to cart."})
class PlaceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        order = Order.objects.create(user=user)

        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart_items.delete()

        return Response({"message": "Order placed successfully!"})


class OrderListAdminView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Order.objects.all()
    
class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class ProductAdminViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class AdminOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-ordered_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    items = request.data.get("items", [])
    
    if not items:
        return Response({"detail": "No items to order"}, status=400)
    
    order = Order.objects.create(customer=request.user)

    for item in items:
        product_id = item.get("product")
        quantity = item.get("quantity")
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            continue
        OrderItem.objects.create(order=order, product=product, quantity=quantity)

    return Response({"detail": "Order placed successfully!"})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_summary(request):
    return Response({
        "users": User.objects.count(),
        "products": Product.objects.count(),
        "orders": Order.objects.count()
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

