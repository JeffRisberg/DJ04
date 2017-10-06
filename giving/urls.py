from django.conf.urls import url
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [

    url(r'^notificationList/(?P<mode>[\w\-]+)/$', views.NotificationListView.as_view(), name='notification_list_view'),

    url(r'^notificationList/all/$', views.NotificationListView.as_view(), name='notification_list_view_all'),
    url(r'^notificationList/unread/$', views.NotificationListView.as_view(), name='notification_list_view_unread'),

    url(r'^notificationList/mark-as-read/(?P<slug>\d+)/$', views.NotificationListViewMarkAsRead.as_view(),
        name='mark_as_read'),
    url(r'^notificationList/mark-as-unread/(?P<slug>\d+)/$', views.NotificationListViewMarkAsUnread.as_view(),
        name='mark_as_unread'),
    url(r'^notificationList/delete/(?P<slug>\d+)/$', views.NotificationListViewDelete.as_view(), name='delete'),

    url(r'^charityList$', views.CharityListView.as_view(), name='charity_list_view'),

    url(r'^charity/(?P<slug>[\w\-]+)/$', views.CharityDetailView.as_view(), name='charity_detail_view'),

    url(r'^donorList$', views.DonorListView.as_view(), name='donor_list_view'),

    url(r'^donationList$', views.DonationListView.as_view(), name='donation_list_view'),

    url(r'^donation/(?P<id>[\w\-]+)/$', views.DonationDetailView.as_view(), name='donation_detail_view'),

    url(r'^donationNew', views.donation_new_view, name='donation_new_view'),

    url(r'^api/notification/(?P<pk>[0-9]+)/$',
        views.NotificationAPIView.as_view(),
        name='notification'),

    url(r'^api/notifications/$',
        views.NotificationsAPIView.as_view(),
        name='notifications'),

    url(r'^api/charity/(?P<pk>[0-9]+)/$',
        views.CharityAPIView.as_view(),
        name='charity'),

    url(r'^api/charities/$',
        views.CharitiesAPIView.as_view(),
        name='charities'),

    url(r'^api/donation/(?P<pk>[0-9]+)/$',
        views.DonationAPIView.as_view(),
        name='donation'),

    url(r'^api/donations/$',
        views.DonationsAPIView.as_view(),
        name='donations'),

    url(r'^api/taggedItems/$',
        views.TaggedItemsAPIView.as_view(),
        name='taggedItems'),

    url(r'^$', views.index, name='home'),
]
