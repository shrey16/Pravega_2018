from django.conf.urls import url

from . import views

app_name = 'registrations'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^bob$', views.bob, name='bob'),
    url(r'^lasya$', views.lasya, name='lasya'),
    url(r'^lasya/video$', views.lasya_video,
        name='lasya_video'),
    url(r'^pis$', views.pis, name='pis'),
    url(r'^pis/video$', views.pis_video,
        name='pis_video'),
    url(r'^footprints$', views.proscenium_streetplay,
        name='proscenium_streetplay'),
    url(r'^proscenium/theatre$', views.proscenium_theatre,
        name='proscenium_theatre'),
    url(r'^proscenium/video$', views.proscenium_theatre_video,
        name='proscenium_theatre_video'),
    url(r'^openmic$', views.openmic, name='openmic'),
    url(r'^decoherence$', views.decoherence, name='decoherence'),
    url(r'^hackathon$', views.hackathon, name='hackathon'),
    url(r'^hackathon/abstract$', views.hackathon_abstract, name='hackathon_abstract'),
]
