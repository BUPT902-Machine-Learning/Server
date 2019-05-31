from django.conf.urls import url
from textInteraction import views as text_interation_views

urlpatterns = [
    # url(r'^api/svmtrain/$', interationViews.API.SVMAPI.trainData),
    # url(r'^api/svmtest/$', interationViews.API.SVMAPI.testData),
    url(r'^knnTrain/$', text_interation_views.API.KnnAPI.train_data),
    url(r'^knnTest/$', text_interation_views.API.KnnAPI.test_data),
    url(r'^cnnTrain/$', text_interation_views.API.CnnAPI.train_data),
    url(r'^cnnTest/$', text_interation_views.API.CnnAPI.test_data),
    url(r'^rnnTrain/$', text_interation_views.API.RnnAPI.train_data),
    url(r'^rnnTest/$', text_interation_views.API.RnnAPI.test_data),
    url(r'^testModel/$', text_interation_views.API.TestOnlyAPI.test_model)
]
