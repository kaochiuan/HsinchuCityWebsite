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
    url(r'^syncInfo$', 'app.views.about', name='about'),
    url(r'^allMyGodsInHsinchu$', 'app.views.allMyGodsInHsinchu', name='allMyGodsInHsinchu'),
    url(r'^addressToLatlng$', 'app.views.address_to_location', name='addressToLatlng'),
    url(r'^templeMaps$', 'app.views.templeMaps', name='templeMaps'),
    url(r'^syncTempleInfo$', 'app.views.syncTempleInfo', name='syncTempleInfo'),
    url(r'^syncCultureInfo$', 'app.views.syncCultureInfo', name='syncCultureInfo'),
    url(r'^syncCityNews$', 'app.views.syncCityNews', name='syncCityNews'),
    url(r'^filterTemple$', 'app.views.filterTemple', name='filterTemple'),
    url(r'^filterCultureActivities$', 'app.views.filterCultureActivities', name='filterCultureActivities'),
    url(r'^cultureActivities$', 'app.views.cultureActivities', name='cultureActivities'),
    url(r'^cityNews$', 'app.views.cityNews', name='cityNews'),
    url(r'^getTop10News$', 'app.views.getTop10News', name='getTop10News'),
    url(r'^animalHospitalReputation$', 'app.views.animalHospitalReputation', name='animalHospitalReputation'),
    url(r'^getReputationOfAnimalHospital$', 'app.views.getReputationOfAnimalHospital', name='getReputationOfAnimalHospital'),
    url(r'^memberPerformance$', 'app.views.memberPerformance', name='memberPerformance'),
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
