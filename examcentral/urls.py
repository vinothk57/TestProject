import os.path
import examcentralapp
from django.conf.urls import *
from django.contrib.auth.views import login
from django.views.static import serve

from django.contrib import admin
admin.autodiscover()

from examcentralapp.views import *
from examcentralapp.forms import LoginForm

site_media = os.path.join(
  os.path.dirname(examcentralapp.__file__), 'site_media'
)
media = os.path.join(
  os.path.dirname(examcentralapp.__file__), 'media'
)


urlpatterns = [
    # Examples:
    # url(r'^$', 'examcentral.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', web_page),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', register_page),
    url(r'^profile/$', profile_page),
    url(r'^myaccount/$', user_loggedin),
    url(r'^history/$', history_page),
    url(r'^analysis/$', analysis_page),
    url(r'^addexam/$', addexam_page),
    url(r'^changeprofilepic/$', model_form_upload),
    url(r'^removeexam/$', removeexam_page),
    url(r'^takeexam/$', takeexam_page),
    url(r'^evaluateexam/$', evalexam_page),
    url(r'^showresult/$', showresult_page),
    url(r'^reviewexam/$', review_page),
    url(r'^analyzeexam/$', analyzegraphs_page),
    url(r'^home/$', main_page),
    url(r'^user/(\w+)/$', user_page),
    url(r'^login/$', login, {'authentication_form': LoginForm}),
    url(r'^logout/$', logout_page),
    url(r'^site_media/(?P<path>.*)$', serve, { 'document_root': site_media }),
    url(r'^media/(?P<path>.*)$', serve, { 'document_root': media }),
    url(r'^search/$', search_page),
    url(r'^getqtn/$', getqtn_page),
    url(r'^fetchpaper/$', fetchQuestionPaperJSON),
    url(r'^getprofiledata/$', get_profile_data),
    url(r'^getgraphdata/$', get_graph_data),
    url(r'^getsectiondata/$', get_section_data),
    url(r'^fetchsolution/$', fetchSolutionJSON),

    # Account Management
    url(r'^createexam/$', examdetails_save_page),
    url(r'^addquestions/$', addquestions_page),
    url(r'^removequestions/$', removequestion_page),
    url(r'^editqtndetail/$', editqtndetail_page),
    url(r'^publishexam/$', publishexam_page),
    url(r'^reset_password/$', ResetPasswordRequestView.as_view(), name="reset_password"),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),

    # Payment

    url(r'^payment/$', payment, name="payment"),
    url(r'^payment/success$', payment_success, name="payment_success"),
    url(r'^payment/failure$', payment_failure, name="payment_failure"),

    # Admin interface
    url(r'^getexamdetails/$', examdetails_page),
    #url(r'^admin/', include('django.contrib.admin.urls')),
]
