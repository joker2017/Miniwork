#import io

from rest_framework import serializers
from .models import Users


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('full_names', 'username', 'email', 'password', 'id')
        read_only_fields = ('id',)
