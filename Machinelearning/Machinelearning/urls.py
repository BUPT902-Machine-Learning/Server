"""Machinelearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from users import views as users_views
from modelOperation import views as model_operation_views
from Machinelearning import settings
from django.conf.urls.static import static
from adaptive import views as adaptive_views

router = routers.DefaultRouter()
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/loginCheck/$', users_views.API.login_check),
    url(r'^api/stuGetModels/$', model_operation_views.API.stu_get_models),
    url(r'^api/teachGetModels/$', model_operation_views.API.teach_get_models),
    url(r'^api/deleteModel/$', model_operation_views.API.delete_model),
    url(r'^api/editModels/$', model_operation_views.API.edit_models),
    url(r'^api/namedCheck/$', model_operation_views.API.named_check),
    url(r'^api/text/', include('textInteraction.urls')),
    url(r'^api/numbers/', include('numbersInteraction.urls')),
    url(r'^api/image/', include('imageInteraction.urls')),
    url(r'^api/text/optimalTrain/$', adaptive_views.API.text_train),
    url(r'^api/numbers/optimalTrain/$', adaptive_views.API.numbers_train),
    # url(r'^api/adaptive/$', adaptiveViews.api.traindata),
    # url(r'^api/adaptivetest/$', adaptiveViews.api.testdata),
    url(r'^api/cooperation/', include('cooperation.urls')),
    url(r'^api/scratch/', include('scratch3.urls')),
    # url(r'^api/createImageModel/$', ImageClassifier_views.API.ImageClassifierAPI.create_model),
    # url(r'^api/trainImageModel/$', ImageClassifier_views.API.ImageClassifierAPI.train_model),
    # url(r'^api/uploadImg/$', ImageClassifier_views.API.ImageClassifierAPI.save_data),
    # url(r'^api/deleteImg/$', ImageClassifier_views.API.ImageClassifierAPI.delete_data),
    # url(r'^api/deleteLabel/$', ImageClassifier_views.API.ImageClassifierAPI.delete_label),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
