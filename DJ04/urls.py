from django.conf.urls import url, include
from django.contrib import admin

import notifications.urls

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^giving/', include('giving.urls', namespace="giving")),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^', include('giving.urls', namespace="giving")),
]

