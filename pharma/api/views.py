from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet, ReadOnlyModelViewSet
from rest_framework.authtoken.serializers import AuthTokenSerializer
from jose import jwt, JWTError

from shop.models import Category, Product
from slugify import slugify

from .serializers import CategorySerializer, CalculatorSerializer, ProductHyperLinkedModelSerializer


class JWTAuthentication(TokenAuthentication):
    keyword = settings.TOKEN_TYPE

    def authenticate_credentials(self, key):
        try:
            payload = jwt.decode(key, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError:
            raise AuthenticationFailed('token invalid')
        else:
            user = get_object_or_404(User, username=payload.get('sub'))
            return user, key


class MyPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'p'


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_staff
        )


class ProductReadOnlyModelViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductHyperLinkedModelSerializer
    queryset = Product.objects.all()


class CalculatorViewSet(ViewSet):
    serializer_class = CalculatorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data={'result': int(request.data.get('height')) * int(request.data.get('width'))})


class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = MyPagination
    permission_classes = [IsAdminUserOrReadOnly]

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST.dict() | {'slug': slugify(request.data.get('name'))})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data.dict() | {'slug': slugify(request.data.get('name'))},
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class JWTAuthViewSet(ViewSet):
    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'sub': request.data.get('username'),
            'exp': datetime.utcnow() + timedelta(minutes=settings.EXPIRE_JWT_TOKEN)
        }
        token = jwt.encode(data, settings.SECRET_KEY)
        return Response({
            'token': token,
            'token_type': settings.TOKEN_TYPE
        })
