from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.fields import IntegerField


from django.utils.crypto import get_random_string


class BigIntegerField(IntegerField):
    empty_strings_allowed=False
    def get_internal_type(self):
        return "BigIntegerField"
    def db_type(self):
        return 'bigint'

class NoisemakerProfile(models.Model):
    BANKS = (
        ('Access Bank Plc', 'Access Bank Plc'),
        ('Diamond Bank Limited', 'Diamond Bank Limited'),
        ('Ecobank Nigeria Plc', 'Ecobank Nigeria Plc'),
        ('Fidelity Bank Plc', 'Fidelity Bank Plc'),
        ('First Bank of Nigeria Plc', 'First Bank of Nigeria Plc'),
        ('First City Monument Bank Ltd', 'First City Monument Bank Ltd'),
        ('Guaranty Trust Bank Plc', 'Guaranty Trust Bank Plc'),
        ('StanbicIBTC Bank', 'StanbicIBTC Bank'),
        ('Skye Bank', 'Skye Bank'),
        ('Standard Chartered Bank Nigeria Ltd', 'Standard Chartered Bank Nigeria Ltd'),
        ('Sterling Bank Plc', 'Sterling Bank Plc'),
        ('Union Bank of Nigeria Plc', 'Union Bank of Nigeria Plc'),
        ('United Bank for Africa Plc', 'United Bank for Africa Plc'),
        ('Unity Bank', 'Unity Bank'),
        ('Wema Bank Plc', 'Wema Bank Plc'),
        ('Zenith International Bank Ltd', 'Zenith International Bank Ltd'),
    )
    PREFERENCES = (

       ('Entertainment,Fashion,Lifestyle', 'Entertainment,Fashion,Lifestyle'),
        ('Internet & Technology', 'Internet & Technology'),
        ('Telecoms & Media', 'Telecoms & Media'),
        ('Health care & Agriculture', 'Health care & Agriculture'),
        ('Real Estate & Hospitality', 'Real Estate & Hospitality'),
        ('Women/Girl Advocacy', 'Women Girl Advocacy'),
        ('Sports', 'Sports'),
        ('Politics', 'Politics'),
        ('Transportation', 'Transportation'),
        ('Financial services', 'Financial services'),
        ('Education', 'Education'),
        ('Aerospace', 'Aerospace'),

    )
    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name=('username'), primary_key=True,)
    twitter_handle = models.CharField(max_length=250, null=True)
    facebook_handle = models.CharField(max_length=250, null=True)
    instagram_handle = models.CharField(max_length=250, null=True)
    twitter_ID = models.BigIntegerField(null=False,  default=0)
    facebook_ID = models.IntegerField(null=False, default=0)
    instagram_ID = models.BigIntegerField(null=False, default=0)
    number_of_friends = models.IntegerField(null=False,verbose_name=('number of friends'), default=0)
    escrow = models.FloatField(null=False,verbose_name=('account'), default=0.0)
    decibel = models.FloatField(null=False,verbose_name=('decibel'), default=0.5)
    account_number = models.IntegerField(null=False, default=0)
    account_name = models.CharField(max_length=250, null=True)
    bank_name = models.CharField(max_length=250, choices=BANKS)
    preferences = models.CharField(max_length=6500)

    class Meta:
        ordering = ["pk"]
        verbose_name = 'Noisemakerz Profile'


    def __str__(self):
        return '%s %s %s %s' % (self.user, self.twitter_handle, self.decibel, self.escrow)

    def rank(self):

        if self.decibel <= 2.5:
            return "Whisperer"
        elif self.decibel <= 7.5:
            return "Jabber"
        elif self.decibel <= 14.5 :
            return "Hypeman"
        elif self.decibel <= 29.5:
            return "Preacher"
        else:
            return "Town Crier"



@python_2_unicode_compatible
class Campaigns(models.Model):
    ACTIONS = (
        ('Retweet', 'Retweet'),
        ('Follow', 'Follow'),
        ('Tweet', 'Tweet'),


    )
    PREFERENCES = (
        ('All' , 'All'),
        ('Entertainment,Fashion,Lifestyle', 'Entertainment,Fashion,Lifestyle'),
        ('Internet & Technology', 'Internet & Technology'),
        ('Telecoms & Media', 'Telecoms & Media'),
        ('Health care & Agriculture', 'Health care & Agriculture'),
        ('Real Estate & Hospitality', 'Real Estate & Hospitality'),
        ('Women/Girl Advocacy', 'Women Girl Advocacy'),
        ('Sports', 'Sports'),
        ('Politics', 'Politics'),
        ('Transportation', 'Transportation'),
        ('Financial services', 'Financial services'),
        ('Education', 'Education'),
        ('Aerospace', 'Aerospace'),

    )
    campaign_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,verbose_name=('user'), on_delete=models.CASCADE)
    base_pay = models.IntegerField(null=False,verbose_name=('base pay'), default=0)
    url = models.CharField(max_length=250, blank=True, null=True, default='')
    action = models.CharField(max_length=100, verbose_name=('action'), choices= ACTIONS)
    tracking_ID = models.CharField(max_length=500, null=True, blank=True)
    tweet = models.CharField(max_length=200, null=True, blank=True, default='')
    follow_handle = models.CharField(max_length=200, blank=True,null=True, default='')
    follow_handle_id = models.CharField(max_length=250, null=True, blank=True)
    hash_tag = models.CharField(max_length=50, blank=True,null=True, default='')
    dummy_tracker = models.CharField(max_length=300, verbose_name=('tracking number'), null=True)
    activity_count = models.IntegerField(null=False, default=0)
    estimated_reach = models.IntegerField(null=False, default=0)
    decibel = models.FloatField(null=False, default=0.5)
    preferences = models.CharField(max_length=6500,)
    budget = models.FloatField(null=False, verbose_name=('budget'), default=0.0)
    influencers_budget = models.FloatField(null=False, verbose_name=('influencers_budget'), default=0.0)
    time_created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(verbose_name=('approved'),default=False)
    funded = models.BooleanField(verbose_name=('funded'),default=False)
    featured = models.BooleanField(default=False)
    lookup = models.SlugField(unique=False,default=get_random_string,max_length=13,)



    def __str__(self):
         return "Campaigns: {0}".format(self.user)

    class Meta:
        ordering = ["campaign_id"]
        verbose_name = 'Campaign'
        db_table = 'Campaign'


class  Tracker(models.Model):
    tracking_ID = models.CharField(verbose_name=('tracking id'),max_length=500)
    campaign = models.ForeignKey(Campaigns,verbose_name=('campaign'), on_delete=models.CASCADE)
    trackers_ID = models.ForeignKey(User,verbose_name=('user'), on_delete=models.CASCADE)
    action_count = models.CharField(max_length=10000)
    tracked = models.BooleanField()

    time_tracked = models

    def get_basepay(self):
        return self.campaign.base_pay

    def __str__(self):
        return '%s %s %s %s' % (self.tracking_ID, self.campaign, self.trackers_ID, self.tracked)

    class Meta:
        db_table = "Activities"
        verbose_name = 'Tracker'



class Payouts(models.Model):
    payout_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,verbose_name=('user'), on_delete=models.CASCADE)
    amount_requested = models.FloatField(null=False,verbose_name=('amount requested'), default=0.0)
    approved = models.BooleanField(verbose_name=('approved'))
    note = models.TextField(verbose_name=('note'),)
    paid = models.BooleanField(verbose_name=('paid'),)
    date_requested = models.DateTimeField(auto_now_add=True,verbose_name=('date requested'),)

    def __str__(self):
     return '%s %s ' % (self.user, self.amount_requested)


    class Meta:
        ordering =["payout_id"]
        db_table = "Influencers Payment"
        verbose_name = 'Noisemakerz Payout'


class Requested(models.Model):
    requested = models.EmailField(unique=True, verbose_name=('e-mail address'),max_length=254)

    def __str__(self):
     return '%s  ' % (self.requested,)

    class Meta:

        verbose_name = 'Request'


