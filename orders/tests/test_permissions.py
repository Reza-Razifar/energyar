from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model

from orders.models import Order
from orders.permissions import OrderPermission


User = get_user_model()


class TestOrderPermission:

    def setup_method(self):
        self.factory = APIRequestFactory()
        self.permission = OrderPermission()

        self.customer = User.objects.create_user(email="customer@email.com", password="test123")
        self.customer.is_customer = True
        self.customer.save()

        self.manager = User.objects.create_user(email="manager@email.com", password="test123")
        self.manager.is_manager = True
        self.manager.save()

        self.order = Order.objects.create(user=self.customer, name="Pizza", quantity=2, total_price=100)

    def test_authenticated_user_has_permission(self):
        request = self.factory.get("/")
        request.user = self.customer

        assert self.permission.has_permission(request,None)

    def test_manager_cannot_post(self):
        request = self.factory.post("/")
        request.user = self.manager

        assert not self.permission.has_permission(request,None)

    def test_customer_can_access_own_order(self):
        request = self.factory.get("/")
        request.user = self.customer

        assert self.permission.has_object_permission(request,None, self.order)

    def test_manager_can_access_any_order(self):
        request = self.factory.get("/")
        request.user = self.manager

        assert self.permission.has_object_permission(request,None, self.order)
