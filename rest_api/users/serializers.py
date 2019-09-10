from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = get_user_model()
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}