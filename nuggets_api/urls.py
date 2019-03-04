from django.conf.urls import url, include
from . import api_controllers

urlpatterns = [
    url(r'^api/v0/user/(?P<user_id>[0-9]+)/nuggets/$', api_controllers.nuggets_op_by_user, name='nuggets_op_by_user'),
    url(r'^api/v0/user/(?P<user_id>[0-9]+)/nuggets/(?P<nugget_id>[0-9]+)$', api_controllers.nuggets_op_by_user_and_nugget, name='nuggets_op_by_user_and_nugget'),
]
