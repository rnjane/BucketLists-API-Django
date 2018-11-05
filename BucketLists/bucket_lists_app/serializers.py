from rest_framework import serializers
from django.contrib.auth.models import User
from bucket_lists_app import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.get('username', None)
        email = validated_data.get('email', None)
        password = validated_data.get('password', None)

        if username and email and password:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            return user
        raise(serializers.ValidationError('Please provide username, email, password and password confirmation'))


class BucketListsSerializer(serializers.ModelSerializer):
    bucket_items = serializers.RelatedField(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = models.BucketListsModel
        fields = ['owner', 'name', 'date_created', 'date_modified', 'bucket_items', 'id']
        

class BucketListItemsSerializer(serializers.ModelSerializer):
    bucketlist = serializers.ReadOnlyField(source='bucketlist.name')
    class Meta:
        model = models.BucketItemsModel
        fields = ['name', 'date_created', 'date_modified', 'bucketlist', 'id']
