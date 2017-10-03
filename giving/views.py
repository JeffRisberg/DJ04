from django.core.context_processors import csrf
from django.http.response import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import Context, loader
from django.views.generic import TemplateView, ListView

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from rest_framework.generics import (
    ListAPIView, RetrieveAPIView
)

from django.contrib.auth.models import User, Group

from notifications.signals import notify
from notifications.models import Notification

from .models import Charity, Donor, Donation
from .serializers import UserSerializer, GroupSerializer, CharitySerializer, DonationSerializer, NotificationSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CharityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows charities to be viewed or edited.
    """
    queryset = Charity.objects.all()
    serializer_class = CharitySerializer


class DonationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows donations to be viewed or edited.
    """
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer


def index(request):
    template = loader.get_template('giving/home.html')
    context = Context()
    output = template.render(context)
    return HttpResponse(output)


class CharityListView(ListView):
    model = Charity


class CharityDetailView(TemplateView):
    template_name = 'giving/charity_detail.html'

    def get_context_data(self, **kwargs):
        return {'charity': Charity.objects.get(slug__iexact=kwargs['slug'])}


class DonorListView(ListView):
    model = Donor


class DonationListView(ListView):
    model = Donation


class DonationDetailView(TemplateView):
    template_name = 'giving/donation_detail.html'

    def get_context_data(self, **kwargs):
        return {'donation': Donation.objects.get(id=kwargs['id'])}


def donation_new_view(request):
    c = {}
    c.update(csrf(request))
    user = getattr(request, "user", None)

    if request.method == 'POST':
        notify.send(user, recipient=user, verb='Submitted donation')
        if int(request.POST['amount']) > 100:
            notify.send(user, recipient=user, verb='Big donation - send thank you email')

        id = int(request.POST['charity'])
        charity = Charity.objects.get(id__iexact=id)

        donation = Donation(donor=user, amount=int(request.POST['amount']), charity=charity)
        donation.save()
        return redirect("/giving/")
    else:
        notify.send(user, recipient=user, verb='Started creation of donation')

    charity_list = Charity.objects.all()
    c.update({'charity_list': charity_list})
    return render_to_response("giving/donation_new.html", c)


class NotificationAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get_object(self):
        return Notification.objects.get(id=self.kwargs['pk'])


class NotificationsAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

