from django.conf.urls import url

from . import views

app_name = 'unbroke'
urlpatterns = [
	url(r'^$', views.IndexView, name='index'),
    url(r'^register$', views.RegisterView, name='register'),
]