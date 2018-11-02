from django.conf.urls import url
from bucket_lists_app import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^register/$', views.UserRegister.as_view(), name='register'),
    url(r'^login/$', views.UserLogin.as_view(), name='login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)