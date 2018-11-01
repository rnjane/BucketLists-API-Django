from django.db import models
from django.contrib.auth.models import User

class BucketListsModel(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, related_name='bucketlists', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['date_created']

class BucketItemsModel(models.Model):
    name = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    bucketlist = models.ForeignKey(BucketListsModel, related_name='bucket_items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['date_created']