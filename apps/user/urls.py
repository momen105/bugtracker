from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('token/', CustomTokenObtainPairView.as_view(), name='access_token'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
