from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from model_mommy import mommy
from . import models

class BaseViewTest(APITestCase):
    def setUp(self):
        client = APIClient()
        self.user = client.post(reverse('register'), {'username': 'test_user1', 'email': 'test1@test.com', 'password': 'testpass'})
        self.user2 = client.post(reverse('register'), {'username': 'test_user2', 'email': 'test2@test.com', 'password': 'testpass'})
        self.my_user = User.objects.get(username='test_user1')
        self.my_user2 = User.objects.get(username='test_user2')
        self.token = Token.objects.create(user=self.my_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.bucketlist = mommy.make(models.BucketListsModel, name='roba', owner=self.my_user)

class UsersTestCase(BaseViewTest):
    def test_user_can_register(self):
        response = self.client.post(reverse('register'), {'username': 'test_user', 'email': 'test@test.com', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_login(self):
        response = self.client.post(reverse('login'), {'username': 'test_user1', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BucketsTestCase(BaseViewTest):
    '''Test cases for the budget model'''
    def test_user_can_create_a_bucket_list(self):
        '''test an authenticated user can create a bucketlist'''
        response = self.client.post(reverse('bucketlists'), {'name': 'testbucket'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_user_can_view_all_bucketlists(self):
        '''test a user can view all their bucketlists'''
        token = Token.objects.create(user=self.my_user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        mommy.make(models.BucketListsModel, owner=self.my_user2, _quantity=10)
        response = self.client.get(reverse('bucketlists'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_a_user_can_edit_a_bucketlist(self):
        mommy.make(models.BucketListsModel, owner=self.my_user)
        response = self.client.patch(reverse('bucket_details', kwargs={'pk': 2}), {'name': 'new bucket name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('new bucket name', response.data['name'])

    def test_a_user_can_delete_a_bucketlist(self):
        mommy.make(models.BucketListsModel, owner=self.my_user)
        response = self.client.delete(reverse('bucket_details', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)


class ItemsTestCase(BaseViewTest):
    def test_a_user_can_create_an_item(self):
        response = self.client.post(reverse('items_view_create', kwargs={'bucketlist_id': 1}), {'name': 'testitem'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_user_can_view_a_single_item(self):
        mommy.make(models.BucketItemsModel, bucketlist=self.bucketlist, name='item1')
        response = self.client.get(reverse('item_details', kwargs={'pk': 1, 'bucketlist_id': 1}))
        self.assertEqual('item1', response.data['name'])

    def test_a_user_can_view_all_items(self):
        mommy.make(models.BucketItemsModel, bucketlist=self.bucketlist, _quantity=10)
        response = self.client.get(reverse('items_view_create', kwargs={'bucketlist_id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_a_user_can_edit_an_item(self):
        bucketlist = mommy.make(models.BucketListsModel, owner=mommy.make(User))
        mommy.make(models.BucketItemsModel, bucketlist=bucketlist)
        response = self.client.patch(reverse('item_details', kwargs={'pk': 1, 'bucketlist_id': 2}), {'name': 'new item name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.BucketItemsModel.objects.get().name, 'new item name')

    def test_a_user_can_delete_an_item(self):
        bucketlist = mommy.make(models.BucketListsModel, owner=mommy.make(User))
        mommy.make(models.BucketItemsModel, bucketlist=bucketlist)
        response = self.client.delete(reverse('item_details', kwargs={'pk': 1, 'bucketlist_id': 2}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_a_user_needs_authorization_for_items_operations(self):
        client = APIClient()
        response = client.get(reverse('items_view_create', kwargs={'bucketlist_id': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)