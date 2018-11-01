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
        confirm_password = validated_data.get('confirm_password', None)

        if username and email and password and confirm_password:
            if password = confirm_password:
                user = User(username=username, email=email)
                user.set_password(password)
                user.save()
                return user
            raise(serializers.ValidationError('passwords do not match!'))
        raise(serializers.ValidationError('Please provide username, email, password and password confirmation'))


class BucketListsSerializer(serializers.ModelSerializer):
    bucket_list_items = serializers.RelatedField(many=True)
    class Meta:
        model = models.BucketListsModel
        fields = ['name', 'date_created', 'date_modified', 'bucket_list_items']
        

class BucketListItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BucketItemsModel
        fields = ['name', 'date_created', 'date_modified', 'bucketlist']
