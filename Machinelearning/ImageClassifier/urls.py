from django.conf.urls import url, include
from ImageClassifier import views as image_classifier_views

urlpatterns = [
    url(r'^techGetImgModel/$', image_classifier_views.ImageClassifierAPI.tech_get_model),
    url(r'^stuGetImgModel/$', image_classifier_views.ImageClassifierAPI.stu_get_model),
    url(r'^techGetCoImgModel/$', image_classifier_views.ImageClassifierAPI.tech_get_co_model),
    url(r'^stuGetCoImgModel/$', image_classifier_views.ImageClassifierAPI.stu_get_co_model),

    url(r'^createImageModel/$', image_classifier_views.ImageClassifierAPI.create_model),
    url(r'^trainImageModel/$', image_classifier_views.ImageClassifierAPI.train_model),
    url(r'^deleteImageModel/$', image_classifier_views.ImageClassifierAPI.delete_model),
    url(r'^testImageModel/$', image_classifier_views.ImageClassifierAPI.test_model),
    url(r'^uploadImg/$', image_classifier_views.ImageClassifierAPI.save_data),
    url(r'^deleteImg/$', image_classifier_views.ImageClassifierAPI.delete_data),
    url(r'^deleteLabel/$', image_classifier_views.ImageClassifierAPI.delete_label),

    url(r'^StatusCheck/$', image_classifier_views.ImageClassifierAPI.train_status_check)
]