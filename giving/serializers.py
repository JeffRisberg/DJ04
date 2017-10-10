from django.contrib.auth.models import User, Group
from notifications.models import Notification
from rest_framework import serializers

from .models import TaggedItem, Charity, Donor, Donation


class ActorSerializer(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize instances with specific serializer.
        """
        if isinstance(value, User):
            serializer = UserSerializer(value, context=self.context)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


class NotificationSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ('id',
                  'recipient', 'level', 'actor',
                  'verb', 'description')


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
                  'name', 'description', 'founded_date', 'website', 'contact')


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


class TaggedObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize instances with specific serializer.
        """
        if isinstance(value, Charity):
            serializer = CharitySerializer(value)
        elif isinstance(value, Donor):
            serializer = DonorSerializer(value)
        elif isinstance(value, Donation):
            serializer = DonationSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


class TaggedItemSerializer(serializers.ModelSerializer):
    tagged_object = TaggedObjectRelatedField(read_only=True)

    class Meta:
        model = TaggedItem
        fields = ('id',
                  'tag_name', 'tagged_object')
