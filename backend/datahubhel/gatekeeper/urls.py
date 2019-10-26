from django.urls import re_path

from . import views

app_name = 'datahubhel.gatekeeper'
urlpatterns = [
    re_path(r'^(?P<path>.*)$', views.Gatekeeper.as_view(), name='index')
]
