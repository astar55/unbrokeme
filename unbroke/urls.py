from django.conf.urls import url

from . import views

app_name = 'unbroke'
urlpatterns = [
	url(r'^$', views.IndexView, name='index'),
    url(r'^login$', views.IndexView2, name='index2'),
    url(r'^register$', views.RegisterView, name='register'),
    url(r'^home$', views.HomeView, name='home'),
]