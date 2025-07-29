from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def cart_items(self):
        return self.cartitem_set.all()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart {self.cart.id}"

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.cart.user.username}"

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  



