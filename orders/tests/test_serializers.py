from django.contrib.auth import get_user_model
from django.test import TestCase

from orders.v1.serializers import OrderSerializer


User = get_user_model()


class OrderSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="customer@email.com", password="test123")

    def test_serializer_valid_data(self):
        payload = {
            "name": "Pizza",
            "quantity": 2,
            "total_price": 100
        }

        serializer = OrderSerializer(data=payload)

        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid_data(self):
        payload = {
            "name": "",
            "quantity": -1
        }

        serializer = OrderSerializer(data=payload)

        self.assertFalse(serializer.is_valid())