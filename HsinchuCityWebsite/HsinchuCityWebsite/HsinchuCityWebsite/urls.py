"""
Definition of urls for HsinchuCityWebsite.
"""

from datetime import datetime
from django.conf.urls import patterns, url, include
from app.forms import BootstrapAuthenticationForm

# Uncomment the next lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^about$', 'app.views.about', name='about'),
    url(r'^allMyGodsInHsinchu$', 'app.views.allMyGodsInHsinchu', name='allMyGodsInHsinchu'),
    url(r'^addressToLatlng$', 'app.views.address_to_location', name='addressToLatlng'),
    url(r'^templeMaps$', 'app.views.templeMaps', name='templeMaps'),
    url(r'^syncTempleInfo$', 'app.views.syncTempleInfo', name='syncTempleInfo'),
    url(r'^filterTemple', 'app.views.filterTemple', name='filterTemple'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
