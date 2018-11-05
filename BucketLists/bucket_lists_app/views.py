from django.shortcuts import render
from rest_framework import generics, views, permissions, response, status, authtoken
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from bucket_lists_app import serializers, models


class UserRegister(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

class UserLogin(views.APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request, format=None):
        serializer = serializers.UserSerializer
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return response.Response({'error': 'please provide both username and password'},
                    status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return response.Response({'error': 'Invalid credentials'},
                    status=status.HTTP_404_NOT_FOUND)
        else:
            token, _ = Token.objects.get_or_create(user=user)
            return response.Response({'token': token.key},
                    status=status.HTTP_200_OK)

class BucketListsViews(views.APIView):
    def post(self, request):
        serialized_bucketlist = serializers.BucketListsSerializer(data=request.data)
        if serialized_bucketlist.is_valid():
            serialized_bucketlist.save(owner=self.request.user)
            return response.Response(serialized_bucketlist.data, status=status.HTTP_201_CREATED)
        return response.Response(serialized_bucketlist.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        bucketlists = models.BucketListsModel.objects.filter(owner=request.user)
        serialized_budgets = serializers.BucketListsSerializer(bucketlists, many=True)
        return response.Response(serialized_budgets.data)


class BucketListDetails(views.APIView):
    def get_bucketlist(self, pk, request):
        return get_object_or_404(models.BucketListsModel, pk=pk, owner=request.user)

    def get(self, request, pk):
        bucketlist = self.get_bucketlist(pk, request)
        serialized_bucketlist = serializers.BucketListsSerializer(bucketlist)
        return response.Response(serialized_bucketlist.data)

    def patch(self, request, pk):
        bucketlist = self.get_bucketlist(pk, request)
        serialized_bucketlist = serializers.BucketListsSerializer(bucketlist, data=request.data)
        if serialized_bucketlist.is_valid():
            serialized_bucketlist.save()
            return response.Response(serialized_bucketlist.data)
        return response.Response(serialized_bucketlist.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bucketlist = self.get_bucketlist(pk, request)
        bucketlist.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ItemsViews(views.APIView):
    def post(self, request, bucketlist_id):
        serialized_item = serializers.BucketListItemsSerializer(data=request.data)
        bucketlist = get_object_or_404(models.BucketListsModel, pk=bucketlist_id, owner=request.user)
        if serialized_item.is_valid():
            serialized_item.save(bucketlist=bucketlist)
            return response.Response(serialized_item.data, status=status.HTTP_201_CREATED)
        return response.Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, bucketlist_id):
        items = models.BucketItemsModel.objects.filter(bucketlist_id=bucketlist_id)
        serialized_items = serializers.BucketListItemsSerializer(items, many=True)
        return response.Response(serialized_items.data)


class ItemDetails(views.APIView):
    def get_item(request, pk, bucketlist_id):
        return get_object_or_404(models.BucketItemsModel, pk=pk, bucketlist_id=bucketlist_id)

    def get(self, request, pk, bucketlist_id):
        item = self.get_item(pk, bucketlist_id)
        serialized_item = serializers.BucketListItemsSerializer(item)
        return response.Response(serialized_item.data)

    def patch(self, request, pk, bucketlist_id):
        item = self.get_item(pk, bucketlist_id)
        serialized_item = serializers.BucketListItemsSerializer(item, data=request.data)
        if serialized_item.is_valid():
            serialized_item.save()
            return response.Response(serialized_item.data)
        return response.Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, bucketlist_id):
        item = self.get_item(pk, bucketlist_id)
        item.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)