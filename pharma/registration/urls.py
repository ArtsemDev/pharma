from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import RegisterView, SignInView

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='signup'),
    path('login/', SignInView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout')
]
