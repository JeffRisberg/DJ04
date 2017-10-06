from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.context_processors import csrf
from django.http.response import HttpResponse
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import Context, loader
from django.views.generic import TemplateView, ListView, RedirectView
from django.utils.decorators import method_decorator

from notifications.models import Notification
from notifications.signals import notify
from rest_framework import viewsets
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated

from .utils import id2slug, slug2id

from .models import TaggedItem, Charity, Donor, Donation
from .serializers import \
    UserSerializer, GroupSerializer, \
    CharitySerializer, DonationSerializer, NotificationSerializer, \
    TaggedItemSerializer


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


class NotificationListView(ListView):
    template_name = 'giving/notification_list.html'
    model = Notification

    def get_queryset(self):
        mode = self.kwargs['mode'] or 'all'
        if mode == 'unread':
            return self.request.user.notifications.unread()
        elif mode == 'read':
            return self.request.user.notifications.read()
        else:
            return self.request.user.notifications.all()

    def get_context_data(self, **kwargs):
        context = super(NotificationListView, self).get_context_data(**kwargs)
        mode = self.kwargs['mode'] or 'all'
        context['mode'] = mode
        return context


class NotificationListViewMarkAsRead(RedirectView):
    permanent = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NotificationListViewMarkAsRead, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        id = slug2id(kwargs['slug'])

        notification = get_object_or_404(Notification, recipient=self.request.user, id=id)
        notification.mark_as_read()

        _next = self.request.GET.get('next')

        if _next:
            self.url = _next
        else:
            self.url = '/giving/notificationList/all'

        return super(NotificationListViewMarkAsRead, self).get_redirect_url(*args, **kwargs)


class NotificationListViewMarkAsUnread(RedirectView):
    permanent = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NotificationListViewMarkAsUnread, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        id = slug2id(kwargs['slug'])

        notification = get_object_or_404(Notification, recipient=self.request.user, id=id)
        notification.mark_as_unread()

        _next = self.request.GET.get('next')

        if _next:
            self.url = _next
        else:
            self.url = '/giving/notificationList/all'

        return super(NotificationListViewMarkAsUnread, self).get_redirect_url(*args, **kwargs)


class NotificationListViewDelete(RedirectView):
    permanent = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NotificationListViewDelete, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        id = slug2id(kwargs['slug'])

        notification = get_object_or_404(Notification, recipient=self.request.user, id=id)
        notification.delete()

        _next = self.request.GET.get('next')

        if _next:
            self.url = _next
        else:
            self.url = '/giving/notificationList/all'

        return super(NotificationListViewDelete, self).get_redirect_url(*args, **kwargs)


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


##############
# API Views
##############

class NotificationAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get_object(self):
        return Notification.objects.get(id=self.kwargs['pk'])


class NotificationsAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class DonationAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DonationSerializer

    def get_object(self):
        return Donation.objects.get(id=self.kwargs['pk'])


class DonationsAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer


class TaggedItemsAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = TaggedItem.objects.all()
    serializer_class = TaggedItemSerializer
