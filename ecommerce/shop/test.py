from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from shop.models import *

User = get_user_model()

class ShopTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='password123')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            category=self.category,
            user=self.user,
            name='Test Product',
            description='Test Description',
            price=100.00
        )
        self.client.login(email='user@example.com', password='password123')

    def test_register(self):
        url = reverse('register')  # Ensure you have this URL
        data = {
            'email': 'test2@example.com',
            'password': 'test12345'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse('login')  # Ensure you have this URL
        data = {
            'email': 'user@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        self.assertEqual(cart_item.quantity, 1)
