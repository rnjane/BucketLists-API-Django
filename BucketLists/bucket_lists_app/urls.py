from django.conf.urls import url
from bucket_lists_app import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^register/$', views.UserRegister.as_view(), name='register'),
    url(r'^login/$', views.UserLogin.as_view(), name='login'),
    url(r'^bucketlists/$', views.BucketListsViews.as_view(), name='bucketlists'),
    url(r'^bucketlist-details/(?P<pk>[0-9]+)/$', views.BucketListDetails.as_view(), name='bucket_details'),
    url(r'^bucketlist/(?P<bucketlist_id>[0-9]+)/items/$', views.ItemsViews.as_view(), name='items_view_create'),
    url(r'^bucketlist/(?P<bucketlist_id>[0-9]+)/items/(?P<pk>[0-9]+)/$', views.ItemDetails.as_view(), name='item_details')
]

# urlpatterns = format_suffix_patterns(urlpatterns)