from rest_framework import serializers
from core.serializers import BulkCreateModelSerializer
from .models import Product, Order


class ProductSerializer(BulkCreateModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(BulkCreateModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        read_only=False
    )

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity')

        if product and quantity:
            if quantity > product.stock:
                raise serializers.ValidationError(
                    f"Insufficient stock. Requested: {quantity}, Available: {product.stock}"
                )
            data['total_price'] = product.price * quantity

        return data