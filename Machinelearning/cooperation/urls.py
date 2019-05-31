from django.conf.urls import url, include
from cooperation import views as cooperation_views

urlpatterns = [
    url(r'^createModel/$', cooperation_views.API.create_model),
    url(r'^stuGetCreateModel/$', cooperation_views.API.stu_get_create_model),
    url(r'^teachGetCreateModel/$', cooperation_views.API.teach_get_create_model),
    url(r'^getModelData/$', cooperation_views.API.get_model_data),
    url(r'^pushData/$', cooperation_views.API.push_data),
    url(r'^trainModel/$', cooperation_views.API.train_model),
    url(r'^ifTrain/$', cooperation_views.API.if_train),
    url(r'^deleteModel/$', cooperation_views.API.delete_model)
]
