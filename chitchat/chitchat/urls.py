from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from messenger import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from chitchat import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('', views.messages_list),
                #   path('api/categories/', views.),
                #   path('api/categories/<int:pk>/', views.),
]