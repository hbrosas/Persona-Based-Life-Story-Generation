from django.conf.urls import url
from clientapp import views
#from clientapp import training_data
#from clientapp import training_data
from clientapp.datacollection import training_data
from clientapp.datacollection import testing_data
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'), # Notice the URL has been named
    url(r'^loading/$', views.LoadPageView.as_view(), name='loading'),
	url(r'^profile/$', views.ProfilePageView.as_view(), name='profile'),
    url(r'^ajax/store_training_data', csrf_exempt(training_data.store_training_data), name='store_training_data'),
    url(r'^ajax/store_testing_data', csrf_exempt(testing_data.store_testing_data), name='store_testing_data'),
]
