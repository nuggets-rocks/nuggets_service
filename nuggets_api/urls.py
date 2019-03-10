from django.conf.urls import url
from rest_framework.authtoken import views as authviews
from . import api_controllers

urlpatterns = [
    url(r'^api/v0/user/(?P<user_id>[0-9]+)/nuggets/$', api_controllers.nuggets_op_by_user, name='nuggets_op_by_user'),
    url(r'^api/v0/user/(?P<user_id>[0-9]+)/nuggets/(?P<nugget_id>[0-9]+)$', api_controllers.nuggets_op_by_user_and_nugget, name='nuggets_op_by_user_and_nugget'),
    url(r'^register/user-name/(?P<user_name>[0-9,a-z,A-Z]+)/password/(?P<password>[0-9,a-z,A-Z]+)$', api_controllers.create_new_user, name='create_new_user'),
    url(r'^api-token-auth/', authviews.obtain_auth_token),
]
