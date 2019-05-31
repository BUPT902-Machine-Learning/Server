from django.conf.urls import url, include
from scratch3 import views as scratch3_views

urlpatterns = [
    url(r'^stuGetModels/$', scratch3_views.API.stu_get_models),
    url(r'^teachGetModels/$', scratch3_views.API.teach_get_models),
    url(r'^stuGetCreateModel/$', scratch3_views.API.stu_get_create_model),
    url(r'^teachGetCreateModel/$', scratch3_views.API.teach_get_create_model),
    url(r'^getLabels/$', scratch3_views.API.get_labels),
    url(r'^useModel/$', scratch3_views.API.use_model),
    url(r'^test/$', scratch3_views.API.test)
]