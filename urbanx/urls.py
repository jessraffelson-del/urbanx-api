from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from city.views import CityServiceViewSet
from marketplace.views import ProductViewSet, OrderViewSet
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

router_v1 = DefaultRouter()
router_v1.register(r'services', CityServiceViewSet, basename='cityservice')
router_v1.register(r'products', ProductViewSet, basename='product')
router_v1.register(r'orders', OrderViewSet, basename='order')

router_v2 = DefaultRouter()
router_v2.register(r'services', CityServiceViewSet, basename='cityservice-v2')
router_v2.register(r'products', ProductViewSet, basename='product-v2')
router_v2.register(r'orders', OrderViewSet, basename='order-v2')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((router_v1.urls, 'v1'), namespace='v1')),
    path('api/v2/', include((router_v2.urls, 'v2'), namespace='v2')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]