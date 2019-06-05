from django.conf.urls import url, include
from cooperation import views as cooperation_views

urlpatterns = [
    url(r'^createTextModel/$', cooperation_views.API.create_text_model),
    url(r'^stuGetCreateModel/$', cooperation_views.API.stu_get_create_model),
    url(r'^teachGetCreateModel/$', cooperation_views.API.teach_get_create_model),
    url(r'^getTextModelData/$', cooperation_views.API.get_text_model_data),
    url(r'^pushTextData/$', cooperation_views.API.push_text_data),
    url(r'^trainTextModel/$', cooperation_views.API.train_text_model),
    url(r'^ifTrain/$', cooperation_views.API.if_train),
    url(r'^deleteModel/$', cooperation_views.API.delete_model)
]
