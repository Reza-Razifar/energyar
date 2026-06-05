from django.test import TestCase

from orders.models import Order
from django.contrib.auth import get_user_model


User = get_user_model()


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="customer@email.com", password="test123")

    def test_order_creation(self):
        order = Order.objects.create(user=self.user, name="Pizza", quantity=2, total_price=100)
        self.assertEqual(order.name,"Pizza")
        self.assertEqual(order.quantity,2)
        self.assertEqual(order.total_price,100)

    def test_order_string_representation(self):
        order = Order.objects.create(user=self.user,name="Pizza", quantity=2, total_price=100)

        self.assertEqual(str(order),"Pizza")
