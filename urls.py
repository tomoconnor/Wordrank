from django.conf.urls.defaults import *
from wordrank.backend.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^wordrank/', include('wordrank.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
	(r'^$', 'wordrank.backend.views.index'),
	(r'^vote/(?P<word_a>(([\w-]|\')+))\/(?P<word_b>(([\w-]|\')+))\/(?P<winner>(\w))','wordrank.backend.views.vote'),
        (r'^favicon.\ico/?', 'django.views.generic.simple.redirect_to', {'url': 'http://media.tomoconnor.eu/tomoconnor/favicon.ico'}),
        (r'^favicon.\png/?', 'django.views.generic.simple.redirect_to', {'url': 'http://media.tomoconnor.eu/tomoconnor/favicon.ico'}),
	(r'^robots\.txt/?', 'django.views.generic.simple.redirect_to', {'url': 'http://media.tomoconnor.eu/tomoconnor/robots.txt'}),


)
