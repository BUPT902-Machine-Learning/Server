from django.conf.urls import url
from textInteraction import views as text_interaction_views
from adaptive import views as adaptive_views
from modelOperation import views as model_operation_views

urlpatterns = [
    # url(r'^api/svmtrain/$', interationViews.API.SVMAPI.trainData),
    # url(r'^api/svmtest/$', interationViews.API.SVMAPI.testData),
    url(r'^knnTrain/$', text_interaction_views.API.KnnAPI.train_data),
    url(r'^knnTest/$', text_interaction_views.API.KnnAPI.test_data),
    url(r'^cnnTrain/$', text_interaction_views.API.CnnAPI.train_data),
    url(r'^cnnTest/$', text_interaction_views.API.CnnAPI.test_data),
    url(r'^rnnTrain/$', text_interaction_views.API.RnnAPI.train_data),
    url(r'^rnnTest/$', text_interaction_views.API.RnnAPI.test_data),
    url(r'^editModel/$', model_operation_views.API.text_edit_model),
    url(r'^testModel/$', text_interaction_views.API.TestOnlyAPI.test_model),
    url(r'^optimalTrain/$', adaptive_views.API.text_train),
]
