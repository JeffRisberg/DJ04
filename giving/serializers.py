from rest_framework import serializers

from django.contrib.auth.models import User, Group

from notifications.models import Notification

from .models import Charity, Donor, Donation


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id',
                  'timestamp', 'level', 'actor_content_type', 'actor_object_id',
                  'verb', 'description',
                  'target_content_type', 'target_object_id')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id',
                  'url', 'name')


class CharitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Charity
        fields = ('id',
                  'name', 'description', 'founded_date', 'website')


class DonorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Donor
        fields = ('id',
                  'first_name', 'last_name')


class DonationSerializer(serializers.ModelSerializer):
    charity = CharitySerializer()
    donor = UserSerializer()

    class Meta:
        model = Donation
        fields = ('id',
                  'created_at', 'charity', 'donor', 'amount')

