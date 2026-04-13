import logging
from core.views import BaseModelViewSet
from .models import CityService
from .serializers import CityServiceSerializer

logger = logging.getLogger(__name__)


class CityServiceViewSet(BaseModelViewSet):
    queryset = CityService.objects.all()
    serializer_class = CityServiceSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create' and isinstance(self.request.data, list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(
            f"Creating city service(s) - bulk: {isinstance(request.data, list)}"
        )
        response = super().create(request, *args, **kwargs)
        logger.info(f"City service created successfully")
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.warning(f"Deleting city service: {instance.name} (id={instance.id})")
        return super().destroy(request, *args, **kwargs)
