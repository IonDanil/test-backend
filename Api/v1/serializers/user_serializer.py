from django.contrib.auth import get_user_model
from rest_framework import serializers

from modelUsers.models import Subscription

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """ Сериализатор пользователей."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Сериализатор подписки."""

    course = serializers.StringRelatedField()
    user = CustomUserSerializer()

    class Meta:
        model = Subscription
        fields = ('id', 'course', 'user', 'group')
