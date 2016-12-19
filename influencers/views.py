from django.shortcuts import render
from django.views.generic.base import TemplateView
import operator
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
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.conf import settings
from django.core import signing
from django.views import View
from .signals import user_recovers_password
from .utils import get_user_model, get_username
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.debug import sensitive_post_parameters

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

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site



class SaltMixin(object):
    salt = 'password_recovery'
    url_salt = 'password_recovery_url'


def loads_with_timestamp(value, salt):
    """Returns the unsigned value along with its timestamp, the time when it
    got dumped."""
    try:
        signing.loads(value, salt=salt, max_age=-999999)
    except signing.SignatureExpired as e:
        age = float(str(e).split('Signature age ')[1].split(' >')[0])
        timestamp = timezone.now() - datetime.timedelta(seconds=age)
        return timestamp, signing.loads(value, salt=salt)
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

def Request(request):
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
            email = EmailMessage("New Request",content,'Noisemakers <do_not_replay@domain.com>',['chukwuemekacharles88@gmail.com', 'office@surkreo.com'],
                headers = {'Reply-To': email_r }
            )
            email.send()

            email2 = EmailMessage("Message from the Class Captain",cont,'Noisemakers <do_not_replay@domain.com>', [email_r],)
            email2.content_subtype = "html"
            email2.send()

            store = Requested(requested=email_r)
            store.save()
            modal01 = 'modal01'
            return render(request, 'index.html', {'modal01': modal01})
        variables ={
            'form' : form
        }

        return render(request, 'influencers/request.html', variables)

def Faq(request):
    return render(request, 'influencers/faq.html')
def Brand(request):
    return render(request, 'influencers/brand.html')
def Influencers(request):
    return render(request, 'influencers/influencers.html')
def error404(request):
    return render(request, 'influencers/404.html')

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
        earn = "%.2f" % 236.0999876
        return render(request, 'index.html' ,{ 'form2' : form2, 'campaigns' : campaigns, 'earn' : earn })



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
            email = EmailMessage("New Request",content,'Noisemakers <do_not_replay@domain.com>',['chukwuemekacharles88@gmail.com', 'office@surkreo.com'],
                headers = {'Reply-To': email_r }
            )
            email.send()

            email2 = EmailMessage("Message from the Class Captain",cont,'Noisemakers <do_not_replay@domain.com>', [email_r],)
            email2.content_subtype = "html"
            email2.send()

            store = Requested(requested=email_r)
            store.save()
            modal01 = 'modal01'
            return render(request, 'index.html', {'modal01': modal01})
        variables ={
            'form' : form
        }

        return render(request, 'index.html', variables)









class NoisemakersView(View):
    form = ValidationForm()


    template_name = 'influencers/noisemakerz_base'

    def get(self, request, *args, **kwargs):
        us = NoisemakerProfile.objects.get(user = request.user)
        form = ValidationForm()
        preferences = us.preferences



        cam= Campaigns.objects.filter(Q(preferences__contains=preferences)| Q(preferences="All"), approved=True,funded = True, ).order_by('-campaign_id')



        context = {'us' : us, 'form' : form, 'cam' : cam ,  }
        return render(request, 'influencers/campaigns.html', context)

    def post(self, request, *args, **kwargs):
        us = NoisemakerProfile.objects.get(user = request.user)

        form = ValidationForm(request.POST)
        tracking_id = request.POST.get('tracking_id', '')
        username = request.user
        #action_count = '23345567'



        if form.is_valid():
            user = User.objects.get(username=username)
            nm_user = NoisemakerProfile.objects.get(user=user)
            user_handle = nm_user.twitter_handle
            trackers_ID = nm_user.twitter_ID
            user_decibel = nm_user.decibel

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





            preferences = us.preferences
            cam= Campaigns.objects.filter(Q(preferences__contains=preferences)| Q(preferences="All"),approved=True,funded = True, ).order_by('-campaign_id')


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
              earn = "%.2f" % int(km * dc)
              reach = nm.number_of_friends
              nm.escrow = nm.escrow + int(earn)


              nm.save()
              modal = 'modal01'

              bp.influencers_budget = bp.influencers_budget - (km * dc)
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
              earn = "%.2f" %  int(km * dc)
              reach = nm.number_of_friends
              nm.escrow = nm.escrow + float(earn)
              modal = 'modal01'


              nm.save()

              bp.influencers_budget = bp.influencers_budget - (km * dc)
              bp.estimated_reach = bp.estimated_reach + int(reach)
              bp.activity_count = bp.activity_count + 1
              bp.save()

              return render(request, 'influencers/campaigns.html', {'cam':cam, 'us':us, 'modal01' : modal, 'earned' : earn, 'form' : form})



        preferences = us.preferences
        cam= Campaigns.objects.filter(Q(preferences__contains=preferences)| Q(preferences="All"),approved=True,funded = True, ).order_by('-campaign_id')
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

            return redirect('influencers/payout.html/')
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
        your_campaigns = Campaigns.objects.filter(user = user ).order_by('-campaign_id')

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
            preference = form.cleaned_data['preference']


            tracking_id = url[-18:]

            budget = int(decibel) * int(base_pay)
            dmm = int(budget)
            influ_budget = 0.7 * dmm

            user = User.objects.get(username=request.user)
            dummy_id  = random.randint(999, 9999) + dmm
            new_campaign=Campaigns(user=user,action=action, dummy_tracker = dummy_id,
                                   follow_handle=follow_handle, hash_tag=hash_tag,
                                   tweet=tweet, url=url, base_pay=base_pay,
                                   decibel=decibel,preferences=preference,budget=budget,
                                   tracking_ID=tracking_id, influencers_budget = influ_budget)
            new_campaign.save()

            return redirect('influencers/create.html')
        user = User.objects.get(username=request.user)
        your_campaigns = Campaigns.objects.filter(user = user ).order_by('-campaign_id')
        all_campaigns = Campaigns.objects.all()
        var= {'form' : form , 'your_campaigns' : your_campaigns, 'all_campaigns' : all_campaigns
        }

        return render(request, 'influencers/create.html', var )
from django.views.generic import DetailView

class CampaignDetail(DetailView):


    queryset = Campaigns.objects.filter()

    def get_object(self):
        # Call the superclass
        object = super(CampaignDetail, self).get_object()
        # Record the last accessed date
        object.last_accessed = timezone.now()
        object.save()
        # Return the object
        return object



class GetStarted(View):
    def get(self, request, *args, **kwargs):
        form = HandleForm()
        return render(request, 'influencers/enter.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = HandleForm(request.POST)


        if form.is_valid():
            twitter_handle = request.POST.get('twitter_handle', '')
            preference = form.cleaned_data['preference']
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




class RecoverDone(SaltMixin, generic.TemplateView):
    template_name = 'influencers/password_reset/reset_sent.html'

    def get_context_data(self, **kwargs):
        ctx = super(RecoverDone, self).get_context_data(**kwargs)
        try:
            ctx['timestamp'], ctx['email'] = loads_with_timestamp(
                self.kwargs['signature'], salt=self.url_salt,
            )
        except signing.BadSignature:
            raise Http404
        return ctx
recover_done = RecoverDone.as_view()


class Recover(SaltMixin, generic.FormView):
    case_sensitive = True
    form_class = PasswordRecoveryForm
    template_name = 'influencers/password_reset/recovery_form.html'
    success_url_name = 'password_reset_sent'
    modal03 = 'modal03'
    email_template_name = 'influencers/password_reset/recovery_email.txt'
    email_subject_template_name = 'influencers/password_reset/recovery_email_subject.txt'
    search_fields = ['username', 'email']

    def get_success_url(self):
        return reverse(self.success_url_name, args=[self.mail_signature], )


    def get_context_data(self, **kwargs):
        kwargs['url'] = self.request.get_full_path()
        return super(Recover, self).get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(Recover, self).get_form_kwargs()
        kwargs.update({
            'case_sensitive': self.case_sensitive,
            'search_fields': self.search_fields,
        })
        return kwargs

    def get_site(self):
        return get_current_site(self.request)

    def send_notification(self):
        context = {
           # 'site': self.get_site(),
            'user': self.user,
            'username': get_username(self.user),
            'token': signing.dumps(self.user.pk, salt=self.salt),
            'secure': self.request.is_secure(),
        }
        body = loader.render_to_string(self.email_template_name,
                                       context).strip()
        subject = loader.render_to_string(self.email_subject_template_name,
                                          context).strip()
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                  [self.user.email])

    def form_valid(self, form):
        self.user = form.cleaned_data['user']
        self.send_notification()
        if (
            len(self.search_fields) == 1 and
            self.search_fields[0] == 'username'
        ):
            # if we only search by username, don't disclose the user email
            # since it may now be public information.
            email = self.user.username
        else:
            email = self.user.email
        self.mail_signature = signing.dumps(email, salt=self.url_salt)
        return super(Recover, self).form_valid(form)
recover = Recover.as_view()


class Reset(SaltMixin, generic.FormView):
    form_class = PasswordResetForm
    token_expires = None
    template_name = 'influencers/password_reset/reset.html'
    success_url = reverse_lazy('password_reset_done')

    def get_token_expires(self):
        duration = getattr(settings, 'PASSWORD_RESET_TOKEN_EXPIRES',
                           self.token_expires)
        if duration is None:
            duration = 3600 * 48  # Two days
        return duration

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = None

        try:
            pk = signing.loads(kwargs['token'],
                               max_age=self.get_token_expires(),
                               salt=self.salt)
        except signing.BadSignature:
            return self.invalid()

        self.user = get_object_or_404(get_user_model(), pk=pk)
        return super(Reset, self).dispatch(request, *args, **kwargs)

    def invalid(self):
        return self.render_to_response(self.get_context_data(invalid=True))

    def get_form_kwargs(self):
        kwargs = super(Reset, self).get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(Reset, self).get_context_data(**kwargs)
        if 'invalid' not in ctx:
            ctx.update({
                'username': get_username(self.user),
                'token': self.kwargs['token'],
            })
        return ctx

    def form_valid(self, form):
        form.save()
        user_recovers_password.send(
            sender=get_user_model(),
            user=form.user,
            request=self.request
        )

        return redirect(self.get_success_url())

reset = Reset.as_view()


class ResetDone(generic.TemplateView):
    template_name = 'influencers/password_reset/recovery_done.html'


reset_done = ResetDone.as_view()


