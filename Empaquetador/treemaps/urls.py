#encoding:utf-8

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'treemaps.views.home', name='home'),
    # url(r'^treemaps/', include('treemaps.foo.urls')),
    url(r'^treemap', 'graficas.views.Treemap'),
    url(r'^$', 'graficas.views.Menu'),
    # url(r'^treemap', 'graficas.views.Inicio'),
	url(r'^etps/$', 'graficas.views.Inte'),
	url(r'^etps/patologias/(?P<patologia>.+)/(?P<mercado>.+)/(?P<espe>.+)/$', 'graficas.views.Tx',  name='tx'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
