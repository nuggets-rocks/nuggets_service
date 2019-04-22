from django.conf.urls import url
from rest_framework.authtoken import views as authviews
from . import api_controllers

urlpatterns = [
    url(r'^api/v0/user/(?P<user_id>[0-9]+)/nuggets/$', api_controllers.nuggets_op_by_user, name='nuggets_op_by_user'),
    url(r'^api/v0/user/(?P<user_id>[0-9]+)/review/$', api_controllers.nuggets_to_review_by_user, name='nuggets_to_review_by_user'),
    url(r'^api/v0/user/(?P<user_id>[0-9]+)/nuggets/(?P<nugget_id>[0-9]+)$', api_controllers.nuggets_op_by_user_and_nugget, name='nuggets_op_by_user_and_nugget'),
    url(r'^api/v0/user/(?P<user_id>[0-9]+)/content/(?P<content>.+)/source/(?P<source>.+)/url/(?P<url>.+)$', api_controllers.create_new_nugget, name='create_new_nugget'),
    url(r'^register/user-name/(?P<user_name>.+)/password/(?P<password>.+)$', api_controllers.create_new_user, name='create_new_user'),
    url(r'^api/v1/authenticate/email/(?P<email>.+)/token/(?P<token>.+)/firstName/(?P<firstName>.+)/lastName/(?P<lastName>.+)/profileUrl/(?P<profileUrl>.+)$', api_controllers.get_or_create_user_v2, name='get_or_create_user_v2'),
    url(r'^login/user-name/(?P<user_name>.+)/password/(?P<password>.+)$', api_controllers.authenticate_user, name='authenticate_user'),
    url(r'^api-token-auth/', authviews.obtain_auth_token),
]
