import hashlib
import json
from django.utils.cache import patch_cache_control
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class CacheControlMixin:
    cache_max_age = 60

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(
            request, response, *args, **kwargs
        )
        if request.method == 'GET' and response.status_code == 200:
            patch_cache_control(
                response,
                max_age=self.cache_max_age,
                private=True
            )
        return response


class ETagMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(
            request, response, *args, **kwargs
        )
        if request.method == 'GET' and response.status_code == 200:
            response_data = json.dumps(
                response.data,
                sort_keys=True,
                default=str
            )
            etag = hashlib.md5(response_data.encode()).hexdigest()
            etag_value = f'"{etag}"'
            response['ETag'] = etag_value

            if_none_match = request.META.get('HTTP_IF_NONE_MATCH')
            if if_none_match and if_none_match == etag_value:
                response.status_code = 304
                response.data = None
                response['Content-Length'] = '0'

        return response


class RateLimitHeadersMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(
            request, response, *args, **kwargs
        )
        if request.method == 'GET':
            throttle_classes = [AnonRateThrottle, UserRateThrottle]
            for throttle_class in throttle_classes:
                throttle = throttle_class()
                throttle.allow_request(request, self)
                if hasattr(throttle, 'history'):
                    remaining = max(
                        0,
                        throttle.num_requests - len(throttle.history)
                    )
                    response['X-RateLimit-Limit'] = throttle.num_requests
                    response['X-RateLimit-Remaining'] = remaining
                    break
        return response