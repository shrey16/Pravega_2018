from django.conf.urls import url

from . import views

app_name = 'registrations'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^proscenium$', views.proscenium, name='proscenium'),
    url(r'^bob$', views.bob, name='bob'),
    url(r'^proscenium/streetplay$', views.proscenium_streetplay, name='proscenium_streetplay'),
    url(r'^proscenium/theatre$', views.proscenium_theatre, name='proscenium_theatre'),
]
