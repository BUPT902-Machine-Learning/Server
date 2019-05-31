from django.conf.urls import url
from numbersInteraction import views as numbers_interation_views

urlpatterns = [
    # url(r'^api/svmtrain/$', interationViews.API.SVMAPI.trainData),
    # url(r'^api/svmtest/$', interationViews.API.SVMAPI.testData),
    url(r'^valueSet/$', numbers_interation_views.API.value_set),
    url(r'^knnTrain/$', numbers_interation_views.API.KnnAPI.train_data),
    url(r'^knnTest/$', numbers_interation_views.API.KnnAPI.test_data),
    url(r'^cnnTrain/$', numbers_interation_views.API.CnnAPI.train_data),
    url(r'^cnnTest/$', numbers_interation_views.API.CnnAPI.test_data),
    url(r'^rnnTrain/$', numbers_interation_views.API.RnnAPI.train_data),
    url(r'^rnnTest/$', numbers_interation_views.API.RnnAPI.test_data),
    url(r'^testModel/$', numbers_interation_views.API.TestOnlyAPI.test_model)
]
