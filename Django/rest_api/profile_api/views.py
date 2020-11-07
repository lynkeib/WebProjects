from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters

from profile_api import serializers
from profile_api import models
from profile_api import permissions


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
            return Response({"message": message}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, pk=None) -> Response:
        """Handle updating an object"""
        return Response(data={"message": "PUT"}, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk=None) -> Response:
        """Handle a partiel update an object"""
        return Response(data={"message": "PATCH"}, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk=None) -> Response:
        """Delete an object"""
        return Response(data={"message": "DELETE"}, status=status.HTTP_200_OK)


class HelloViewSet(viewsets.ViewSet):
    """Test Api ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request: Request) -> Response:
        """Retrun hellp message"""
        a_viewset = [
            "Uses actions: list, create, retrieve, update, partial_update, destroy",
            "Automatically maps to URLs using Routers",
            "Provides more functionality with less code",
        ]
        return Response(data={"message": "Hello", "an_apiview": a_viewset}, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Hello {name}"
            return Response({"message": message}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request: Request, pk=None) -> Response:
        """Handle getting an object by its ID"""
        return Response(data={"message": "GET"}, status=status.HTTP_200_OK)

    def update(self, request: Request, pk=None) -> Response:
        """Handle updating an object"""
        return Response(data={"message": "PUT"}, status=status.HTTP_200_OK)

    def partial_update(self, request: Request, pk=None) -> Response:
        """Handle updating part of an object"""
        return Response(data={"message": "PATCH"}, status=status.HTTP_200_OK)

    def destroy(self, request: Request, pk=None) -> Response:
        """Handle removing an object"""
        return Response(data={"message": "DELETE"}, status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "email",)
