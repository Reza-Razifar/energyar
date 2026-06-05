from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from . import serializers
from orders import models, permissions


AUTH_HEADER = OpenApiParameter(
    name="Authorization",
    type=str,
    location=OpenApiParameter.HEADER,
    required=True,
    description=(
        "Bearer token.\n"
        "Example: Bearer eyJhbGc..."
    ),
)

class Orders(APIView):
    permission_classes = [permissions.OrderPermission]

    @extend_schema(
        summary="Get orders",
        description="""
            Returns a list of orders.

            Customers only see their own orders.
            Admins can see all orders.
            """,
        parameters=[
            AUTH_HEADER,
            OpenApiParameter(
                name="ordering",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Sort orders by field",
                required=False,
                enum=[
                    "created_at",
                    "total_price"
                ],
                default="created_at"
            ),
            OpenApiParameter(
                name="ascending",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Sort direction",
                required=False,
                enum=[
                    "true",
                    "false"
                ],
                default="false"
            ),
        ],
        responses={
            200: serializers.OrderSerializer(many=True),
            400: OpenApiResponse(description="Invalid parameter"),
        },
        tags=["Orders"],
    )
    def get(self, request):
        user = request.user

        ordering = self.request.query_params.get('ordering', "created_at")
        if ordering not in ("created_at", "total_price"):
            return Response({"message": "invalid parameter"}, status=status.HTTP_400_BAD_REQUEST)

        ascending = self.request.query_params.get('ascending', "false")
        if ascending not in ("true", "false"):
            return Response({"message": "invalid parameter"}, status=status.HTTP_400_BAD_REQUEST)

        order_by = "" if ascending == "true" else "-"

        order_by += ordering

        if user.is_customer:
            orders = models.Order.objects.filter(user=user)
        else:
            orders = models.Order.objects.all()

        orders = orders.order_by(order_by)


        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create order",
        description="""
            Create a new order.
            
            Only customers can create an order.
        """,
        parameters=[
            AUTH_HEADER
        ],
        request=serializers.OrderSerializer,
        responses={
            201: serializers.OrderSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
        tags=["Orders"],
    )
    def post(self, request):
        serializer = serializers.OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    permission_classes = [permissions.OrderPermission]


    def get_object(self, pk):
        return get_object_or_404(models.Order, id=pk)

    @extend_schema(
        summary="Get order detail",
        description="""
            Retrieve order by ID.
            
            Customers only see their own orders.
        """,
        parameters=[
            AUTH_HEADER
        ],
        responses={
            200:serializers.OrderSerializer,
            404:OpenApiResponse(description="Order not found"),
        },
        tags=["Orders"],
    )
    def get(self, request, pk):
        order = self.get_object(pk)

        self.check_object_permissions(request, order)
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update order",
        description="""
            Customers only update their own orders.
        """,
        parameters=[
            AUTH_HEADER
        ],
        request=serializers.OrderSerializer,
        responses={
            200: serializers.OrderSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Order not found"),
        },
        tags=["Orders"],
    )
    def put(self, request, pk):
        order = self.get_object(pk)

        self.check_object_permissions(request, order)
        serializer = serializers.OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete order",
        description="""
            Customers only delete their own orders.
        """,
        parameters=[
            AUTH_HEADER
        ],
        responses={
            204: OpenApiResponse(),
            404:
                OpenApiResponse(description="Order not found"),
        },
        tags=["Orders"],
    )
    def delete(self, request, pk):
        order = self.get_object(pk)

        self.check_object_permissions(request, order)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
