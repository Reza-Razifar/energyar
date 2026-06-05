from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from orders.models import Order


User = get_user_model()


class BaseOrderTestCase(APITestCase):

    def setUp(self):
        # Customer
        self.customer = User.objects.create_user(email="customer1@email.com", password="test123")
        self.customer.save()

        # Another customer
        self.other_customer = User.objects.create_user(email="customer2@email.com", password="test123")
        self.other_customer.save()

        # Manager
        self.manager = User.objects.create_user(email="manager1@email.com", password="test123", role="manager")
        self.manager.save()

        # Orders
        self.order = Order.objects.create(user=self.customer, name="Pizza", quantity=2, total_price=100)

        self.other_order = Order.objects.create(user=self.other_customer, name="Burger", quantity=1, total_price=50)
