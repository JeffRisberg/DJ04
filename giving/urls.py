from django.conf.urls import url
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^api/notification/(?P<pk>[0-9]+)/$',
        views.NotificationAPIView.as_view(),
        name='notification'),

    url(r'^api/notifications/$',
        views.NotificationsAPIView.as_view(),
        name='notifications'),

    url(r'^charityList$', views.CharityListView.as_view(), name='charity_list_view'),

    url(r'^charity/(?P<slug>[\w\-]+)/$', views.CharityDetailView.as_view(), name='charity_detail_view'),

    url(r'^donorList$', views.DonorListView.as_view(), name='donor_list_view'),

    url(r'^donationList$', views.DonationListView.as_view(), name='donation_list_view'),

    url(r'^donation/(?P<id>[\w\-]+)/$', views.DonationDetailView.as_view(), name='donation_detail_view'),

    url(r'^donationNew', views.donation_new_view, name='donation_new_view'),

    url(r'^$', views.index, name='home'),
]
