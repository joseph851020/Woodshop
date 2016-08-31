from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.indexView,
        name='index'
    ),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        name='login',
        kwargs={'template_name':'lumberyard/login.html'}
    ),
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        name='logout',
        kwargs={'next_page': '/'}
    ),
    url(
        r'^jobSearch/$',
        views.ajaxjobsearch,
        name='jobSearch'
    ),
    url(
        r'^jobDetail/(?P<job_id>\d+)/$',
        views.JobDetailView,
        name='jobDetail'
    ),
    url(
        r'^sequenceSearch/$',
        views.ajaxsequencesearch,
        name='sequenceSearch'
    ),
    url(
        r'^jobDetail/(?P<job_id>\d+)/sequenceDetail/(?P<sequence_id>\d+)/$',
        views.sequenceDetailView,
        name='sequenceDetail'
    ),
    url(
        r'^renderSearch/$',
        views.ajaxrendersearch,
        name='renderSearch'
    ),
]
