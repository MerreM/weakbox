from django.conf.urls import patterns, url

urlpatterns = patterns('drawer.views',
    # Examples:
    # url(r'^$', 'weakbox.views.home', name='home'),
    url(r'^register/$','registerApplication',name="register"),
    url(r'^store/(?P<key>\w{1,20})/(?P<value>\w{0,100})/$','storeValue',name="store"),
    url(r'^retrieve/(?P<key>\w{1,20})/$','retrieveValue',name="retrieve"),
    url(r'^retrieve/$','retrieveAll',name="retrieveAll"),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
