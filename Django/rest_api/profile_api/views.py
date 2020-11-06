from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from profile_api import serializers


# Create your views here.
class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request: Request, format: str = None) -> Response:
        """Returns a list of APIView features"""
        an_apiview = [
            "Uses HTTP methods as function (get, post, patch, put, delete)",
            "Is similar to a traditional Django View",
            "Gives you the most control over your application logic",
            "Is mapped manually to URLs",
        ]
        return Response(data={"message": "Hello", "an_apiview": an_apiview}, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Hello {name}"
            return Response({"message": message})
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, pk=None) -> Response:
        """Handle updating an object"""
        return Response(data={"message": "PUT"})

    def patch(self, request: Request, pk=None) -> Response:
        """Handle a partiel update an object"""
        return Response(data={"message": "PATCH"})

    def delete(self, request: Request, pk=None) -> Response:
        """Delete an object"""
        return Response(data={"message": "DELETE"})
