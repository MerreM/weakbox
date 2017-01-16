from django.conf.urls import url
from drawer.views import register_application
from drawer.views import store_value
from drawer.views import retrieve_value
from drawer.views import retrieve_all


urlpatterns = [
    url(r'^register/$', register_application, name="register"),
    url(r'^store/(?P<key>\w{1,20})/(?P<value>\w{0,100})/$',
        store_value, name="store"),
    url(r'^retrieve/(?P<key>\w{1,20})/$',
        retrieve_value, name="retrieve"),
    url(r'^retrieve/$', retrieve_all, name="retrieve_all"),
]
