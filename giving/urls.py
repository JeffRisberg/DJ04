from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^charityList$', views.charity_list_view, name='charity_list_view'),
    url(r'^donorList$', views.donor_list_view, name='donor_list_view'),
    url(r'^donationList$', views.donation_list_view, name='donation_list_view'),
    url(r'^newDonation', views.new_donation_view, name='new_donation_view'),
    url(r'^$', views.index, name='index'),
]