from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^submitFeature$', views.get_feature, name='submitFeature'),
	url(r'^accessFeature$', views.access_feature_response, name='accessFeature')
]