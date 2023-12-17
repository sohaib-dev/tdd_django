from django.urls import path

from . import views

urlpatterns = [
    path(r'^(?P<pk>\d+)/$', views.EntryDetail.as_view(), name='entry_detail'),
]
