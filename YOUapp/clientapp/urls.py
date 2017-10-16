from django.conf.urls import url
from clientapp import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'), # Notice the URL has been named
    url(r'^loading/$', views.LoadPageView.as_view(), name='loading'),
	url(r'^profile/$', views.ProfilePageView.as_view(), name='profile'),
]
