
from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^charityList$', views.charity_list_view, name='charity_list_view'),
    url(r'^charity/(?P<slug>[\w\-]+)/$', views.charity_detail_view, name='charity_detail_view'),
    url(r'^donorList$', views.donor_list_view, name='donor_list_view'),
    url(r'^donationList$', views.donation_list_view, name='donation_list_view'),
    url(r'^donationNew', views.donation_new_view, name='donation_new_view'),
    url(r'^$', views.index, name='home'),
]