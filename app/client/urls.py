from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from client import (
    views
)

router = DefaultRouter()
router.register('client_api', views.ClientView, basename='client_api')

app_name = 'client'

urlpatterns = [
    path('', include(router.urls)),
]
