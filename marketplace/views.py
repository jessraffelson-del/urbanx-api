import logging
from rest_framework.decorators import action
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from core.views import BaseModelViewSet
from core.responses import APIResponse
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

logger = logging.getLogger(__name__)


class ProductViewSet(BaseModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create' and isinstance(self.request.data, list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_products = Product.objects.filter(is_available=True, stock__gt=0)
        serializer = self.get_serializer(available_products, many=True)
        return APIResponse.success(
            data=serializer.data,
            message="Available products retrieved successfully"
        )

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        product = self.get_object()
        orders = Order.objects.filter(product=product)
        serializer = OrderSerializer(orders, many=True)
        return APIResponse.success(
            data=serializer.data,
            message="Product orders retrieved successfully"
        )


class OrderViewSet(BaseModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create' and isinstance(self.request.data, list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(
            f"Creating order - bulk: {isinstance(request.data, list)}"
        )
        response = super().create(request, *args, **kwargs)
        logger.info("Order created successfully")
        return response

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        logger.info(f"Confirming order id={order.id} for {order.customer_email}")

        if order.status != 'pending':
            logger.warning(
                f"Failed to confirm order id={order.id} - status is {order.status}"
            )
            return APIResponse.error(
                message="Order cannot be confirmed",
                errors=f"Cannot confirm order with status: {order.status}"
            )

        order.status = 'confirmed'
        product = order.product
        product.stock -= order.quantity
        product.save()
        order.save()

        logger.info(
            f"Order id={order.id} confirmed - "
            f"product={product.name}, "
            f"quantity={order.quantity}, "
            f"remaining_stock={product.stock}"
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'marketplace_orders',
            {
                'type': 'order_update',
                'message': {
                    'event': 'order_confirmed',
                    'order_id': order.id,
                    'product': order.product.name,
                    'quantity': order.quantity,
                    'total_price': str(order.total_price)
                }
            }
        )

        return APIResponse.success(
            data=OrderSerializer(order).data,
            message="Order confirmed successfully"
        )