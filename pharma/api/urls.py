from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import CategoryModelViewSet, ProductReadOnlyModelViewSet, CalculatorViewSet, JWTAuthViewSet

router = SimpleRouter()
router.register('category', CategoryModelViewSet)
router.register('product', ProductReadOnlyModelViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/calculator/', CalculatorViewSet.as_view({'post': 'create'})),
    path('auth/', JWTAuthViewSet.as_view({'post': 'create'}))
]
