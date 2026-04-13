import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from city.models import CityService


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def city_service():
    return CityService.objects.create(
        name="Test Library",
        service_type="library",
        description="A test library service",
        location="123 Test Street",
        is_active=True
    )


@pytest.mark.django_db
class TestCityServiceEndpoints:
    def test_list_services(self, api_client):
        response = api_client.get('/api/v1/services/')
        assert response.status_code == 200
        assert response.data['success'] is True
        assert response.data['message'] == 'Retrieved successfully'

    def test_create_service(self, api_client):
        data = {
            'name': 'City Bus Network',
            'service_type': 'transportation',
            'description': 'A bus network',
            'location': 'Central Hub',
            'is_active': True
        }
        response = api_client.post('/api/v1/services/', data, format='json')
        assert response.status_code == 201
        assert response.data['success'] is True
        assert response.data['data']['name'] == 'City Bus Network'

    def test_retrieve_service(self, api_client, city_service):
        response = api_client.get(f'/api/v1/services/{city_service.id}/')
        assert response.status_code == 200
        assert response.data['data']['name'] == 'Test Library'

    def test_update_service(self, api_client, city_service):
        data = {
            'name': 'Updated Library',
            'service_type': 'library',
            'description': 'Updated description',
            'location': '123 Test Street',
            'is_active': True
        }
        response = api_client.put(
            f'/api/v1/services/{city_service.id}/',
            data,
            format='json'
        )
        assert response.status_code == 200
        assert response.data['data']['name'] == 'Updated Library'

    def test_delete_service(self, api_client, city_service):
        response = api_client.delete(f'/api/v1/services/{city_service.id}/')
        assert response.status_code == 200
        assert response.data['message'] == 'Deleted successfully'

    def test_bulk_create_services(self, api_client):
        data = [
            {
                'name': 'Service One',
                'service_type': 'clinic',
                'description': 'First service',
                'location': 'Location One',
                'is_active': True
            },
            {
                'name': 'Service Two',
                'service_type': 'event',
                'description': 'Second service',
                'location': 'Location Two',
                'is_active': True
            }
        ]
        response = api_client.post('/api/v1/services/', data, format='json')
        assert response.status_code == 201
        assert len(response.data['data']) == 2

    def test_invalid_service_type(self, api_client):
        data = {
            'name': 'Bad Service',
            'service_type': 'invalid_type',
            'description': 'This should fail',
            'location': 'Nowhere',
            'is_active': True
        }
        response = api_client.post('/api/v1/services/', data, format='json')
        assert response.status_code == 400