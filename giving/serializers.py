from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Charity, Donor, Donation


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CharitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Charity
        fields = ('name', 'description', 'founded_date', 'website')


class DonorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Donor
        fields = ('first_name', 'last_name')


class DonationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Donation
        fields = ('created_at', 'charity', 'donor', 'amount')
