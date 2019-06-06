from django.conf.urls import url, include
from cooperation import views as cooperation_views

urlpatterns = [
    url(r'^stuGetCreateModel/$', cooperation_views.API.stu_get_create_model),
    url(r'^teachGetCreateModel/$', cooperation_views.API.teach_get_create_model),

    # text cooperation
    url(r'^createTextModel/$', cooperation_views.API.create_text_model),
    url(r'^getTextModelData/$', cooperation_views.API.get_text_model_data),
    url(r'^pushTextData/$', cooperation_views.API.push_text_data),
    url(r'^trainTextModel/$', cooperation_views.API.train_text_model),
    url(r'^textIfTrain/$', cooperation_views.API.text_if_train),
    url(r'^deleteTextModel/$', cooperation_views.API.delete_text_model),

    # numbers cooperation
    url(r'^createNumbersModel/$', cooperation_views.API.create_numbers_model),
    url(r'^getNumbersModelData/$', cooperation_views.API.get_numbers_model_data),
    url(r'^pushNumbersData/$', cooperation_views.API.push_numbers_data),
    url(r'^trainNumbersModel/$', cooperation_views.API.train_numbers_model),
    url(r'^numbersModelGetValue/$', cooperation_views.API.numbers_model_get_value),
    url(r'^numbersIfTrain/$', cooperation_views.API.numbers_if_train),
    url(r'^deleteNumbersModel/$', cooperation_views.API.delete_numbers_model),

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
