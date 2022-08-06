from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import login_api, register_api

urlpatterns = [
    path("register/", register_api, name="register"),
    path("login/", login_api, name="login"),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]
