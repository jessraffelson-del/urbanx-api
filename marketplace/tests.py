import pytest
from rest_framework.test import APIClient
from marketplace.models import Product, Order


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def product():
    return Product.objects.create(
        name="Test Book",
        category="book",
        description="A test book",
        price=29.99,
        stock=10,
        is_available=True
    )


@pytest.fixture
def order(product):
    return Order.objects.create(
        product=product,
        quantity=2,
        total_price=59.98,
        status="pending",
        customer_name="Test Customer",
        customer_email="test@example.com"
    )


@pytest.mark.django_db
class TestProductEndpoints:
    def test_list_products(self, api_client):
        response = api_client.get('/api/v1/products/')
        assert response.status_code == 200
        assert response.data['success'] is True

    def test_create_product(self, api_client):
        data = {
            'name': 'New Gadget',
            'category': 'gadget',
            'description': 'A cool gadget',
            'price': '49.99',
            'stock': 5,
            'is_available': True
        }
        response = api_client.post('/api/v1/products/', data, format='json')
        assert response.status_code == 201
        assert response.data['data']['name'] == 'New Gadget'

    def test_retrieve_product(self, api_client, product):
        response = api_client.get(f'/api/v1/products/{product.id}/')
        assert response.status_code == 200
        assert response.data['data']['name'] == 'Test Book'

    def test_available_products(self, api_client, product):
        response = api_client.get('/api/v1/products/available/')
        assert response.status_code == 200
        assert response.data['success'] is True
        assert len(response.data['data']) >= 1

    def test_invalid_category(self, api_client):
        data = {
            'name': 'Bad Product',
            'category': 'invalid_category',
            'description': 'Should fail',
            'price': '9.99',
            'stock': 1,
            'is_available': True
        }
        response = api_client.post('/api/v1/products/', data, format='json')
        assert response.status_code == 400

    def test_bulk_create_products(self, api_client):
        data = [
            {
                'name': 'Bulk Product One',
                'category': 'book',
                'description': 'First bulk product',
                'price': '19.99',
                'stock': 5,
                'is_available': True
            },
            {
                'name': 'Bulk Product Two',
                'category': 'gadget',
                'description': 'Second bulk product',
                'price': '39.99',
                'stock': 3,
                'is_available': True
            }
        ]
        response = api_client.post('/api/v1/products/', data, format='json')
        assert response.status_code == 201
        assert len(response.data['data']) == 2


@pytest.mark.django_db
class TestOrderEndpoints:
    def test_list_orders(self, api_client):
        response = api_client.get('/api/v1/orders/')
        assert response.status_code == 200
        assert response.data['success'] is True

    def test_create_order(self, api_client, product):
        data = {
            'product': product.id,
            'quantity': 1,
            'customer_name': 'Jane Doe',
            'customer_email': 'jane@example.com',
            'status': 'pending'
        }
        response = api_client.post('/api/v1/orders/', data, format='json')
        assert response.status_code == 201
        assert response.data['data']['customer_name'] == 'Jane Doe'
        assert response.data['data']['total_price'] == '29.99'

    def test_confirm_order(self, api_client, order):
        response = api_client.post(f'/api/v1/orders/{order.id}/confirm/')
        assert response.status_code == 200
        assert response.data['data']['status'] == 'confirmed'

    def test_confirm_already_confirmed_order(self, api_client, order):
        api_client.post(f'/api/v1/orders/{order.id}/confirm/')
        response = api_client.post(f'/api/v1/orders/{order.id}/confirm/')
        assert response.status_code == 400
        assert response.data['success'] is False

    def test_insufficient_stock(self, api_client, product):
        data = {
            'product': product.id,
            'quantity': 999,
            'customer_name': 'Jane Doe',
            'customer_email': 'jane@example.com',
            'status': 'pending'
        }
        response = api_client.post('/api/v1/orders/', data, format='json')
        assert response.status_code == 400

    def test_product_orders(self, api_client, product, order):
        response = api_client.get(f'/api/v1/products/{product.id}/orders/')
        assert response.status_code == 200
        assert len(response.data['data']) == 1