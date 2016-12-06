from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.views.decorators.http import condition
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from influencers.models import *
from django.contrib.auth.models import User
from django.template import Context, Template
from influencers.forms import *
from django.shortcuts import redirect
from django.views import View

from noisemaker_invite import app_settings
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from registration import signals
from django.contrib.auth import authenticate, login
import datetime
from django_modalview.generic.edit import ModalFormView
from django_modalview.generic.component import ModalResponse
import tweepy
import random
from noisemaker_invite.models import Invitation
from noisemaker_invite.exceptions import AlreadyInvited, AlreadyAccepted, UserRegisteredEmail
from noisemaker_invite.app_settings import app_settings
from noisemaker_invite.adapters import get_invitations_adapter
from noisemaker_invite.signals import invite_accepted

auth = tweepy.OAuthHandler('SAl4SONvtBOOzYDLkrdRO3zuk', 'lBXUK6QtPt2O7PvIB4CInac9BpuDf8mZK6rGW5nyPJco3M77tm')
auth.set_access_token('782935264318656512-cQT9cFhG3QQCFCcRHggfxfEh8b0t586', 'KpukwklmsuAtS4et5vQcv4ZDxHtqrsuJyqczg3MN5PhFy')

api = tweepy.API(auth)
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

class SignUpView(View):
    def get(self, request, *arg, **kwargs):

        form = RegistrationForm()
        return render(request, 'influencers/sign_up.html', {'form' : form ,} )


    def post(self, request, *arg, **kwargs):
        form = RegistrationForm(data = request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']




            user = User.objects.create_user(
            username=username,
            password=password,
            email=email
            )
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            new_noisemaker = NoisemakerProfile.objects.create(user=new_user )

            return redirect('start')
        var= {'form' : form
        }

        return render(request, 'influencers/sign_up.html', var )


class HomeViews(View):

    form2 = RequestInviteForm()

    template_name = 'index.html'


    def get(self, request, *args, **kwargs):

        form2 = RequestInviteForm()
        campaigns = Campaigns.objects.filter(featured=True)
        return render(request, 'index.html' ,{ 'form2' : form2, 'campaigns' : campaigns })



    def post(self, request, *args, **kwargs):
        form = RequestInviteForm(data = request.POST)
        if form.is_valid():
            email_r = form.cleaned_data['email']
            twitter_handle = request.POST.get('twitter_handle', '')
            template = get_template('influencers/messages/invited')
            template2 = get_template('influencers/messages/html.html')
            context = Context({
                'email': email_r,
                'twitter_handle': twitter_handle,

            })
            cont = template2.render()
            content = template.render(context)
            email = EmailMessage("New Request",content,'Noisemakers <do_not_replay@domain.com>',['chukwuemekacharles88@gmail.com'],
                headers = {'Reply-To': email_r }
            )
            email.send()

            email2 = EmailMessage("Thank You",cont,'Noisemakers <do_not_replay@domain.com>', [email_r],)
            email2.content_subtype = "html"
            email2.send()

            store = Requested(requested=email_r)
            store.save()
			gotten = 'modal01'
            return render(request, 'index.html',{'modal01':modal01})
        variables ={
            'form' : form
        }

        return render(request, 'index.html', variables)









class NoisemakersView(View):
    form = ValidationForm()


    template_name = 'influencers/campaigns.html'

    def get(self, request, *args, **kwargs):
        us = NoisemakerProfile.objects.filter(user = request.user)
        form = ValidationForm()
        cam= Campaigns.objects.filter(approved=True)


        context = {'us' : us, 'form' : form, 'cam' : cam ,  }
        return render(request, 'influencers/campaigns.html', context)

    def post(self, request, *args, **kwargs):
        us = NoisemakerProfile.objects.filter(user = request.user)

        form = ValidationForm(request.POST)
        tracking_id = request.POST.get('tracking_id', '')
        username = request.user
        #action_count = '23345567'



        if form.is_valid():
            user = User.objects.get(username=username)
            nm_user = NoisemakerProfile.objects.get(user=user)
            user_handle = nm_user.twitter_handle
            trackers_ID = nm_user.twitter_ID

            campaign = Campaigns.objects.get(dummy_tracker=tracking_id)
            track = campaign.tracking_ID
            dummy = campaign.dummy_tracker

            hash_tag = campaign.hash_tag
            #handle_id = api.get_user(handle).id
            #campaign.follow_handle_id = handle_id
            url = campaign.url
            action = campaign.action


            if action == 'Retweet':
                action_count =api.retweeters(id = track, count = 200)
            elif action == 'Follow':
                handle = campaign.follow_handle
                action_count = api.followers_ids(screen_name= handle, count = 5000)
            elif action == 'Tweet':
                ty = api.get_user(id = trackers_ID)

                action_count = ty.status.text



            cam= Campaigns.objects.filter(approved=True)


            chc = Tracker.objects.filter(trackers_ID=user, tracking_ID=dummy ).exists()
            errorclass4 = 'alert alert-success'
            already_tracked = '* Already confirm'

            if chc == True:
             return  render(request, 'influencers/campaigns.html', {'alreadytracked' : already_tracked, 'cam' : cam ,'errorclass4' : errorclass4,  'us':us})
            if hash_tag in action_count:


              category = Tracker(tracking_ID = dummy, trackers_ID = username, action_count=action_count,
                                campaign =campaign, tracked = 'True')
              category.save()

              bp = Campaigns.objects.get( dummy_tracker = dummy)

              km = bp.base_pay

              nm = NoisemakerProfile.objects.get(user = username)
              dc = nm.decibel
              earn = km * dc
              reach = nm.number_of_friends
              nm.escrow = nm.escrow + (km * dc)


              nm.save()
              modal = 'modal01'

              bp.budget = bp.budget - (km * dc)
              bp.estimated_reach = bp.estimated_reach + int(reach)
              bp.activity_count = bp.activity_count + 1
              bp.save()



              return render(request, 'influencers/campaigns.html', {'cam' :cam, 'us':us, 'modal01' : modal, 'earned' : earn,'form' : form})


            elif  trackers_ID in action_count:
              category = Tracker(tracking_ID = dummy, trackers_ID = username, action_count=action_count,
                                campaign =campaign, tracked = 'True')
              category.save()

              bp = Campaigns.objects.get( dummy_tracker = dummy)

              km = bp.base_pay

              nm = NoisemakerProfile.objects.get(user = username)
              dc = nm.decibel
              earn = km * dc
              reach = nm.number_of_friends
              nm.escrow = nm.escrow + (km * dc)
              modal = 'modal01'


              nm.save()

              bp.budget = bp.budget - (km * dc)
              bp.estimated_reach = bp.estimated_reach + int(reach)
              bp.activity_count = bp.activity_count + 1
              bp.save()

              return render(request, 'influencers/campaigns.html', {'cam':cam, 'us':us, 'modal01' : modal, 'earned' : earn, 'form' : form})


        cam = Campaigns.objects.filter(approved=True)
        noaction = 'Yet to carryout the action'
        errorclass5 = 'alert alert-danger'
        variables = {
         'errorclass5' : errorclass5,
        'us' : us,
        'noaction':noaction,
        'form': form,
        'cam' :cam,

    }

        return render(request,'influencers/campaigns.html/', variables)

class PayoutView(View):

    def get(self, request, *args, **kwargs):
        username = request.user
        us = NoisemakerProfile.objects.get(user = username)
        selected = us.bank_name
        usernum = us.account_number
        payment_history = Payouts.objects.filter(user = username)
        form = PayoutForm(initial={'id_bank_account': usernum, 'bank':selected})
        #context = {'us' : us, 'form' : form , 'usernum' : usernum}
        return render(request, 'influencers/payout.html', {'us' : us, 'form' : form , 'usernum' : usernum, 'selected' : selected, 'payment_history' : payment_history})

    def post(self, request, *args, **kwargs):

        form = PayoutForm(request.POST)
        amount = request.POST.get('amount_requested', '')
        username = User.objects.get(username = request.user)
        us = NoisemakerProfile.objects.get(user = username)
        usernum = us.account_number


        balance = us.escrow
        error= 'Minimum request is 500'
        error2 = 'You don'+ "'t" + " " + 'have sufficient balance'
        error3 = 'Minimum Request is 1000'
        error_class = 'alert alert-danger'
        error_class1 = 'alert alert-danger'
        error_class3 = 'alert alert-danger'
        payment_history = Payouts.objects.filter(user = username)



        new_bank = request.POST.get('bank', '')
        new_num = request.POST.get('bank_account', '')


        if int(amount) > balance:
            return render(request, 'influencers/payout.html', {'error2' : error2, 'form' : form, 'error_class' : error_class,
                                                               'payment_history' : payment_history, 'usernum':usernum})
        if int(amount) < 1000:
            return render(request, 'influencers/payout.html', {'error3' : error3, 'form' : form, 'error_class3' : error_class3,
                                                               'payment_history' : payment_history, 'usernum':usernum})

        if form.is_valid():
            pay = Payouts(user = username, amount_requested = amount, approved= False, paid = False, note= 'waiting approval', date_requested = datetime)
            pay.save()
            us.escrow = balance - int(amount)
            us.bank_name = new_bank
            us.account_number = new_num
            us.save()

            return redirect('index')
        us = NoisemakerProfile.objects.get(user = username)
        selected = us.bank_name
        usernum = us.account_number

        context = { 'us' : us, 'form' : form , 'selected' : selected, 'usernum' : usernum}

        return  render(request,'influencers/payout.html/', context)



class ActivitiesView(View):

 def get(self, request, *args, **kwargs):
    username = User.objects.get(username = request.user)

    vg = Tracker.campaign
    real = Tracker.objects.filter(trackers_ID = username)










    return  render(request, 'influencers/activity.html', {  'username' : username ,'real' : real  })


class SummaryView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.get(username=request.user)
        nsp = NoisemakerProfile.objects.get(user=users)
        real = Tracker.objects.filter(trackers_ID = users)

        return render(request, 'influencers/dashboard.html', {'user': users, 'nsp' : nsp,'real' : real})

class CreateCampaignView(View):

    def get(self, request, *arg, **kwargs):
        user = User.objects.get(username=request.user)
        your_campaigns = Campaigns.objects.filter(user = user )
        form = CampaignForm()
        return render(request, 'influencers/create.html', {'form' : form , 'your_campaigns' : your_campaigns} )
    def post(self, request, *arg, **kwargs):
        form = CampaignForm(request.POST)

        if form.is_valid():
            url = request.POST.get('url', '')
            action = request.POST.get('action', '')
            decibel = request.POST.get('decibel', '')
            base_pay = request.POST.get('base_pay', '')
            hash_tag = request.POST.get('hash_tag', '')
            tweet = request.POST.get('tweet', '')
            follow_handle = request.POST.get('follow_handle', '')
            preference = request.POST.get('preference', '')


            tracking_id = url[-18:]

            budget = int(decibel) * int(base_pay)
            dmm = int(budget)

            user = User.objects.get(username=request.user)
            dummy_id  = random.randint(999, 9999) + dmm
            new_campaign=Campaigns(user=user,action=action, dummy_tracker = dummy_id,
                                   follow_handle=follow_handle, hash_tag=hash_tag,
                                   tweet=tweet, url=url, base_pay=base_pay,
                                   decibel=decibel,preferences=preference,budget=budget,
                                   tracking_ID=tracking_id)
            new_campaign.save()

            return redirect('index.html')
        var= {'form' : form
        }

        return render(request, 'influencers/create.html', var )

class GetStarted(View):
    def get(self, request, *args, **kwargs):
        form = HandleForm()
        return render(request, 'influencers/enter.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = HandleForm(request.POST)
        twitter_handle = request.POST.get('twitter_handle', '')
        preference = request.POST.get('preference', '')

        if form.is_valid():
            user = request.user
            twitter_ID = api.get_user(twitter_handle).id
            number_of_friends= api.get_user(twitter_handle).followers_count
            decibel = number_of_friends / 2000
            nf = int(number_of_friends)
            update_nm = NoisemakerProfile(user=user, twitter_handle=twitter_handle,twitter_ID=twitter_ID,decibel=decibel, number_of_friends=nf, preferences=preference)
            update_nm.save()

            return redirect('dashboard')
        variable = {
        'form' : form

          }
        return render(request, 'influencers/enter.html',variable)


