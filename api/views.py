from rest_framework import viewsets, generics, permissions, serializers, status
from rest_framework.response import Response
from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer, UserSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.db.models import Avg
from django.contrib.auth import authenticate
from rest_framework.views import APIView

class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Product.objects.all().annotate(
            average_rating=Avg('reviews__rating')
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs['product_pk']
        return Review.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs['product_pk']
        user = self.request.user
        if Review.objects.filter(product_id=product_id, user=user).exists():
            raise serializers.ValidationError("You have already reviewed this product.")

        serializer.save(user=user, product_id=product_id)


class BrowsableLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'is_staff': user.is_staff
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
