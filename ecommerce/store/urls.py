from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', SignupView.as_view(), name='signup'), 
    path('login/', LoginView.as_view(), name='login'),  
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('me/', MeView.as_view(), name='me'),  # Only one /me/ path should exist


]
