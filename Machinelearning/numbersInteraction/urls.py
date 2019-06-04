from django.conf.urls import url
from numbersInteraction import views as numbers_interaction_views
from adaptive import views as adaptive_views
from modelOperation import views as model_operation_views

urlpatterns = [
    # url(r'^api/svmtrain/$', interationViews.API.SVMAPI.trainData),
    # url(r'^api/svmtest/$', interationViews.API.SVMAPI.testData),
    url(r'^valueSet/$', numbers_interaction_views.API.value_set),
    url(r'^knnTrain/$', numbers_interaction_views.API.KnnAPI.train_data),
    url(r'^knnTest/$', numbers_interaction_views.API.KnnAPI.test_data),
    url(r'^cnnTrain/$', numbers_interaction_views.API.CnnAPI.train_data),
    url(r'^cnnTest/$', numbers_interaction_views.API.CnnAPI.test_data),
    url(r'^rnnTrain/$', numbers_interaction_views.API.RnnAPI.train_data),
    url(r'^rnnTest/$', numbers_interaction_views.API.RnnAPI.test_data),
    url(r'^editModel/$', model_operation_views.API.numbers_edit_model),
    url(r'^testModelGetValue/$', model_operation_views.API.test_model_get_value),
    url(r'^testModel/$', numbers_interaction_views.API.TestOnlyAPI.test_model),
    url(r'^optimalTrain/$', adaptive_views.API.numbers_train),
]
