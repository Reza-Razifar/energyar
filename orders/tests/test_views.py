from django.urls import reverse
from rest_framework import status

from orders.tests.base import BaseOrderTestCase


class OrderViewTest(BaseOrderTestCase):

    # ==========================
    # LIST
    # ==========================

    def test_customer_gets_only_own_orders(self):
        self.client.force_authenticate(user=self.customer)

        response = self.client.get(reverse("orders"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)

    def test_manager_gets_all_orders(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.get(reverse("orders"))

        self.assertEqual(len(response.data), 2)

    # ==========================
    # CREATE
    # ==========================

    def test_customer_can_create_order(self):
        self.client.force_authenticate(user=self.customer)

        payload = {
            "name": "Burger",
            "quantity": 3,
            "total_price": 150
        }

        response = self.client.post(reverse("orders"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_manager_cannot_create_order(self):
        self.client.force_authenticate(user=self.manager)

        payload = {
            "name": "Burger",
            "quantity": 3,
            "total_price": 150
        }

        response = self.client.post(reverse("orders"), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ==========================
    # DETAIL
    # ==========================

    def test_customer_can_get_own_order(self):
        self.client.force_authenticate(user=self.customer)

        response = self.client.get(
            reverse("order_detail", kwargs={"pk": self.order.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_cannot_get_other_order(self):
        self.client.force_authenticate(user=self.customer)

        response = self.client.get(
            reverse(
                "order_detail",
                kwargs={
                    "pk":
                    self.other_order.id
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ==========================
    # UPDATE
    # ==========================

    def test_customer_can_update_order(self):
        self.client.force_authenticate(user=self.customer)

        payload = {
            "name": "Updated Pizza",
            "quantity": 5,
            "total_price": 200
        }

        response = self.client.put(
            reverse(
                "order_detail",
                kwargs={"pk": self.order.id}
            ),
            payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ==========================
    # DELETE
    # ==========================

    def test_customer_can_delete_order(self):
        self.client.force_authenticate(user=self.customer)

        response = self.client.delete(
            reverse(
                "order_detail",
                kwargs={"pk": self.order.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
