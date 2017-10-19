from django.conf.urls import url

from . import views

app_name = 'registrations'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^proscenium$', views.proscenium, name='proscenium'),
]
