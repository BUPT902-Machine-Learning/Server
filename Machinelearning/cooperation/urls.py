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
    url(r'^deleteModel/$', cooperation_views.API.delete_model),

    # image cooperation
    url(r'^createImageModel/$', cooperation_views.API.create_image_model),
    url(r'^stuGetCreateImageModel/$', cooperation_views.API.stu_get_create_image_model),
    url(r'^teachGetCreateImageModel/$', cooperation_views.API.teach_get_create_image_model),
    url(r'^getImageModelData/$', cooperation_views.API.get_image_model_data),
    url(r'^pushImageData/$', cooperation_views.API.push_image_data),
    url(r'^popImageData/$', cooperation_views.API.pop_image_data),
    url(r'^trainImageModel/$', cooperation_views.API.train_image_model),
    url(r'^ifImageTrain/$', cooperation_views.API.if_image_train),
    url(r'^deleteImageModel/$', cooperation_views.API.delete_image_model),
    url(r'^deleteImageLabel/$', cooperation_views.API.delete_image_label),
    url(r'^testImageModel/$', cooperation_views.API.test_image_model),

]
