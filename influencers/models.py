from django.db import models
from django.contrib.auth.models import User
import datetime

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
        ('Fashion and Lifestyle', 'Fashion and Lifestyle'),
        ('Sports, Politics and Education', 'Sports, Politics and Education'),
        ('Technology', 'Technology'),
        ('All', 'All'),

    )
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True,)
    twitter_handle = models.CharField(max_length=250, null=True)
    facebook_handle = models.CharField(max_length=250, null=True)
    instagram_handle = models.CharField(max_length=250, null=True)
    twitter_ID = models.CharField(null=False, max_length=540, default=0)
    facebook_ID = models.IntegerField(null=False, default=0)
    instagram_ID = models.IntegerField(null=False, default=0)
    number_of_friends = models.IntegerField(null=False, default=0)
    escrow = models.FloatField(null=False, default=0.0)
    decibel = models.FloatField(null=False, default=0.5)
    account_number = models.IntegerField(null=False, default=0)
    account_name = models.CharField(max_length=250, null=True)
    bank_name = models.CharField(max_length=250, choices=BANKS, null=True)
    preferences = models.CharField(max_length=250, choices=PREFERENCES, null=True)

    def __str__(self):
        return '%s %s %s %s' % (self.user, self.twitter_handle, self.decibel, self.escrow)

def rank(self):

        if self.decibel <= 1.0:
            return "Whisperer"
        elif self.decibel <= 2.0:
            return "Jabber"
        elif self.decibel <= 4.0 :
            return "Hypeman"
        elif self.decibel <= 5.0:
            return "Preacher"
        else:
            return "Town Crier"



class Campaigns(models.Model):
    ACTIONS = (
        ('Retweet', 'Retweet'),
        ('Follow', 'Follow'),
        ('Tweet', 'Tweet'),


    )
    PREFERENCES = (
        ('All' , 'All'),
        ('Fashion and Lifestyle', 'Fashion and Lifestyle'),
        ('Sports, Politics and Education', 'Sports, Politics and Education'),
        ('Technology', 'Technology'),


    )
    campaign_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    base_pay = models.IntegerField(null=False, default=0)
    url = models.CharField(max_length=250, blank=True, null=True, default='')
    action = models.CharField(max_length=100, choices= ACTIONS)
    tracking_ID = models.CharField(max_length=500, null=True, blank=True)
    tweet = models.CharField(max_length=200, null=True, blank=True, default='')
    follow_handle = models.CharField(max_length=200, blank=True,null=True, default='')
    follow_handle_id = models.CharField(max_length=250, null=True, blank=True)
    hash_tag = models.CharField(max_length=50, blank=True,null=True, default='')
    dummy_tracker = models.CharField(max_length=300, null=True)
    activity_count = models.IntegerField(null=False, default=0)
    estimated_reach = models.IntegerField(null=False, default=0)
    decibel = models.FloatField(null=False, default=0.5)
    preferences = models.CharField(max_length=250, choices=PREFERENCES)
    budget = models.FloatField(null=False, default=0.0)
    time_created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    def __str__(self):
         return "Campaigns: {0}".format(self.user)

    class Meta:
        ordering = ["campaign_id"]
        db_table = "Campaign"

class  Tracker(models.Model):
    tracking_ID = models.CharField(max_length=500)
    campaign = models.ForeignKey(Campaigns, on_delete=models.CASCADE)
    trackers_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    action_count = models.CharField(max_length=10000)
    tracked = models.BooleanField()

    time_tracked = models

    def get_basepay(self):
        return self.campaign.base_pay

    def __str__(self):
        return '%s %s %s %s' % (self.tracking_ID, self.campaign, self.trackers_ID, self.tracked)

    class Meta:
        db_table = "Activities"



class Payouts(models.Model):
    payout_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_requested = models.FloatField(null=False, default=0.0)
    approved = models.BooleanField()
    note = models.TextField()
    paid = models.BooleanField()
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
     return '%s %s ' % (self.user, self.amount_requested)


    class Meta:
        ordering =["payout_id"]
        db_table = "Influencers Payment"


class Requested(models.Model):
    requested = models.EmailField(unique=True, verbose_name=('e-mail address'),max_length=254)

