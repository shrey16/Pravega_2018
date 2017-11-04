from django.conf.urls import url

from . import views

app_name = 'registrations'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^bob$', views.bob, name='bob'),
    url(r'^lasya$', views.lasya, name='lasya'),
    url(r'^pis$', views.pis, name='pis'),
    url(r'^footprints$', views.proscenium_streetplay, name='proscenium_streetplay'),
    url(r'^proscenium/theatre$', views.proscenium_theatre, name='proscenium_theatre'),
]
