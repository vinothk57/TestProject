import os.path
import examcentralapp
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from examcentralapp.views import *
from examcentralapp.forms import LoginForm

site_media = os.path.join(
  os.path.dirname(examcentralapp.__file__), 'site_media'
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'examcentral.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', register_page),
    url(r'^myaccount/$', user_loggedin),
    url(r'^addexam/$', addexam_page),
    url(r'^removeexam/$', removeexam_page),
    url(r'^takeexam/$', takeexam_page),
    url(r'^$', main_page),
    url(r'^user/(\w+)/$', user_page),
    url(r'^login/$', 'django.contrib.auth.views.login', {'authentication_form': LoginForm}),
    url(r'^logout/$', logout_page),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': site_media }),
    url(r'^search/$', search_page),
    url(r'^getqtn/$', getqtn_page),
    url(r'^fetchpaper/$', fetchQuestionPaperJSON),

    # Account Management
    url(r'^createexam/$', examdetails_save_page),
    url(r'^addquestions/$', addquestions_page),
    url(r'^publishexam/$', publishexam_page),

    # Admin interface
    #url(r'^admin/', include('django.contrib.admin.urls')),
)
