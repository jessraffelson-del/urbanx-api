from rest_framework.response import Response
from rest_framework import status


class APIResponse:
    @staticmethod
    def success(data=None, message="Success", status_code=status.HTTP_200_OK):
        return Response({
            "success": True,
            "message": message,
            "data": data,
            "error": None
        }, status=status_code)

    @staticmethod
    def created(data=None, message="Created successfully"):
        return Response({
            "success": True,
            "message": message,
            "data": data,
            "error": None
        }, status=status.HTTP_201_CREATED)

    @staticmethod
    def error(message="An error occurred", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        return Response({
            "success": False,
            "message": message,
            "data": None,
            "error": errors
        }, status=status_code)

    @staticmethod
    def not_found(message="Resource not found"):
        return Response({
            "success": False,
            "message": message,
            "data": None,
            "error": None
        }, status=status.HTTP_404_NOT_FOUND)