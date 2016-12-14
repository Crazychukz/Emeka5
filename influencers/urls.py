__author__ = 'CrazychukZ'
import registration.views
from django.conf.urls import url, include
from influencers.views import NoisemakersView
from Noisemakers import settings
from influencers.views import PayoutView, ActivitiesView, SummaryView, CreateCampaignView, GetStarted, HomeViews, SignUpView

from noisemaker_invite.views import SendInvite
from . import views

urlpatterns = [
    url(r'^$', HomeViews.as_view(), name='index'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^account/register/', SignUpView.as_view(), name='sign_up'),
    #url(r'^requested/', views.contact, name='inn'),
    url(r'^campaigns/', NoisemakersView.as_view(), name='campaigns'),
    url(r'^payout/', PayoutView.as_view(), name='payout'),
    url(r'^activity/', ActivitiesView.as_view(), name='activity'),
    url(r'^dashboard/', SummaryView.as_view(), name='dashboard'),
    url(r'^create/', CreateCampaignView.as_view(), name='create'),
    url(r'^get/', GetStarted.as_view(), name='start'),
    url(r'^recover/(?P<signature>.+)/$', views.recover_done,name='password_reset_sent'),
    url(r'^recover/$', views.recover, name='password_reset_recover'),
    url(r'^reset/done/$', views.reset_done, name='password_reset_done'),
    url(r'^reset/(?P<token>[\w:-]+)/$', views.reset,name='password_reset_reset'),
    url(r'^faq/', views.Faq, name='faq'),
    url(r'^brands/', views.Brand, name='brands'),
    url(r'^influencers/', views.Influencers, name='influencers'),
]
