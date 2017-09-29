
from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^charityList$', views.charity_list_view, name='charity_list_view'),
    url(r'^charity/(?P<slug>[\w\-]+)/$', views.charity_view, name='charity_view'),
    url(r'^donorList$', views.donor_list_view, name='donor_list_view'),
    url(r'^donationList$', views.donation_list_view, name='donation_list_view'),
    url(r'^newDonation', views.new_donation_view, name='new_donation_view'),
    url(r'^$', views.index, name='index'),
]