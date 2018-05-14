from django.conf.urls import url
from apollo.views import log_in, log_out, user_list, sign_up


urlpatterns = [
    url(r'^$', user_list, name='user_list'),
    url(r'^log_in/$', log_in, name='log_in'),
    url(r'^log_out/$', log_out, name='log_out'),
    url(r'^sign_up/$', sign_up, name='sign_up'),
]