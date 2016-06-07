from django.conf.urls import url, patterns
from . import views

urlpatterns = [
	url(r'^submitDC$', views.get_process, name='submit Distributed Computing'),
	url(r'^runDC$', views.get_run, name='Access Distributed Computing'),
	url(r'^', views.not_found, name="Page Not Found")
]