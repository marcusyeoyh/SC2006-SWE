from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer, FavouriteSerializer
from .models import User, Favourite
from rest_framework.authentication import BasicAuthentication
from rest_framework import generics, status
from django.contrib.auth import login

# Class based view to get user details using Basic Authentication
class UserDetailAPI(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# Class based view for user registration
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny),
    serializer_class = UserSerializer

# Class based view for user login
class LoginView(APIView):
    # This view should be accessible also for unauthenticated users
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(
            data=self.request.data,
            context = { 'request': self.request }
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

# Class based view for adding to favourites
class FavouriteView(APIView):
    def get(self, request):
        try:
            favourites = Favourite.objects.filter(email=request.user.email)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = FavouriteSerializer(favourites, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = FavouriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)