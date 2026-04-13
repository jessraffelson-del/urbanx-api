from core.views import BaseModelViewSet
from .models import CityService
from .serializers import CityServiceSerializer


class CityServiceViewSet(BaseModelViewSet):
    queryset = CityService.objects.all()
    serializer_class = CityServiceSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create' and isinstance(self.request.data, list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)
