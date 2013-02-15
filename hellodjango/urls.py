from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^users/', include('warmup.urls', namespace="warmup")),
    url(r'^TESTAPI/', include('warmup.urls', namespace="warmup")),
    # Examples:
    # url(r'^$', 'hellodjango.views.home', name='home'),
    # url(r'^hellodjango/', include('hellodjango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    )

urlpatterns += patterns('', (
	r'^static/(?P<path>.*)$',
	'django.views.static.serve',
	{'document_root': 'static'}
	))