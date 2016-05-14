from django.conf.urls import url

from . import views

app_name = 'unbroke'
urlpatterns = [
	url(r'^$', views.IndexView, name='index'),
    url(r'^register/$', views.RegisterView, name='register'),
    url(r'^home/$', views.HomeView, name='home'),
    url(r'^logout/$', views.LogoutView, name='logout'),
    url(r'^deposits/$', views.DepositsView, name='deposits'),
    url(r'^expenses/$', views.ExpensesView, name='expenses'),
    url(r'^wish/$', views.WishView, name='wish'),
    url(r'^setting/$', views.SettingView, name='setting'),
]