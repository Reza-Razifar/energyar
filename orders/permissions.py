from rest_framework.permissions import BasePermission

from orders.models import Order


class OrderPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and request.user.is_manager:
            return False
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_manager:
            return True

        return obj.user == user
