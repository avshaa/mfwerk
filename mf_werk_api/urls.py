#from django.conf.urls import url
from django.urls import path, include
#from rest_framework import routers
from .views import (
    PartListApiView,
    PartDetailApiView,
)

#router = routers.DefaultRouter()
#router.register(r'upload', UploadViewSet, basename="upload")

urlpatterns = [
    path('api', PartListApiView.as_view()),
    path('api/<int:part_id>', PartDetailApiView.as_view()),
]