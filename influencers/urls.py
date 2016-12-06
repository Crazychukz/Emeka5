__author__ = 'CrazychukZ'
import registration.views
from django.conf.urls import url, include
from influencers.views import NoisemakersView
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


]