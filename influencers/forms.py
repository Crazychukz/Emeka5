__author__ = 'CrazychukZ'

"""
Forms and validation code for user registration.

"""


from django.contrib.auth.models import User
from django import forms
from .models import *
from django.conf import settings
from django.core.validators import validate_email
from django.db.models import Q
from .utils import get_user_model

from django.utils.translation import ugettext_lazy as _
from noisemaker_invite.models import Invitation
from django.contrib.auth import get_user_model
from noisemaker_invite.adapters import get_invitations_adapter
from noisemaker_invite.exceptions import AlreadyInvited, AlreadyAccepted, UserRegisteredEmail, AlreadyRequested


# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = {'class': 'required'}

class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.

    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password (again)"))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("A user with that username already exists."))
    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))

        if Invitation.objects.filter(email__iexact=self.cleaned_data['email']).exists() == False:
            raise forms.ValidationError(_("no invite"))
        return self.cleaned_data['email']



    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.

    """
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={'required': _("You must agree to the terms to register")})


class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.

    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']


class RegistrationFormNoFreeEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which disallows registration with
    email addresses from popular free webmail services; moderately
    useful for preventing automated spam registrations.

    To change the list of banned domains, subclass this form and
    override the attribute ``bad_domains``.

    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com']

    def clean_email(self):
        """
        Check the supplied email address against a list of known free
        webmail domains.

        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_("Registration using free email addresses is prohibited. Please supply a different email address."))
        return self.cleaned_data['email']

class ValidationForm(forms.Form):


    tracking_id = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict,maxlength=18)), label=_("tracking_id"))
    def clean_tracking_id(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        tracking_id = self.cleaned_data.get('tracking_id')

        exists = Campaigns.objects.filter(dummy_tracker=tracking_id).exists()
        if exists == False:
            raise forms.ValidationError("no campaign")

        return self.cleaned_data['tracking_id']
class PayoutForm(forms.Form):
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

    amount_requested = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=250)), label=_("amount_requested"))
    bank_account = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=10)),label=_("bank_account"))
    bank = forms.CharField(widget=forms.Select(choices= BANKS,),  label=_("bank"))

    def check_balance(self):

        amount_requested = self.cleaned_data.get('amount_requested')
        balance = NoisemakerProfile.escrow
        if amount_requested > balance:
            raise forms.ValidationError("You don't have enough")
        elif balance < 5000:
            raise forms.ValidationError("Your Minimum Balance is not up to 5000")
        return self.cleaned_data['amount_requested']


class CampaignForm(forms.Form):
    ACTIONS = (
        ('Retweet', 'Retweet'),
        ('Follow', 'Follow'),
        ('Tweet', 'Tweet')
    )
    PREFERENCES = (
        ('All' , 'All'),
        ('Fashion and Lifestyle', 'Fashion and Lifestyle'),
        ('Sports, Politics and Education', 'Sports, Politics and Education'),
        ('Technology', 'Technology'),

    )
    base_pay = forms.CharField(widget=forms.TextInput)
    url = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict,maxlength=250)),required=False, label=_("url"))
    action = forms.CharField(widget=forms.RadioSelect(choices=ACTIONS), label=_("action"), required=True)
    decibel = forms.IntegerField(widget=forms.TextInput)
    tweet = forms.CharField(required=False)
    hash_tag = forms.CharField(required=False)
    follow_handle = forms.CharField(required=False)
    preference = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=PREFERENCES), label=_("preference"))

    def clean_url(self):
        url = self.cleaned_data["url"]

        return url


    def clean_tweet(self):
        tweet = self.cleaned_data["tweet"]

        return tweet


    def clean_hash_tag(self):
        hash_tag = self.cleaned_data["hash_tag"]

        return hash_tag



    def clean_field(self):
        data = self.cleaned_data['follow_handle']


        return data








class HandleForm(forms.Form):
    PREFERENCES = (

        ('Fashion and Lifestyle', 'Fashion and Lifestyle'),
        ('Sports, Politics and Education', 'Sports, Politics and Education'),
        ('Technology', 'Technology'),

    )

    twitter_handle = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    preference = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=PREFERENCES), required=True, label=_("preference"))



class RequestInviteForm(forms.Form):
    twitter_handle = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    def validate_invitation(self, email):
        if Invitation.objects.all_valid().filter(
                email__iexact=email, accepted=False):
            raise AlreadyInvited
        elif Invitation.objects.filter(
                email__iexact=email, accepted=True):
            raise AlreadyAccepted
        elif Requested.objects.filter(requested__iexact=email):
            raise AlreadyRequested
        elif get_user_model().objects.filter(email__iexact=email):
            raise UserRegisteredEmail
        else:
            return True

    def clean_email(self):
        email = self.cleaned_data["email"]
        email = get_invitations_adapter().clean_email(email)

        errors = {
            "already_invited": _("This e-mail address has already been"
                                 " invited."),
            "already_accepted": _("This e-mail address has already"
                                  " accepted an invite."),
            "email_in_use": _("An active user is using this e-mail address"),
            "has requested": _("This email has requested an invite already"),
        }
        try:
            self.validate_invitation(email)
        except (AlreadyRequested):
            raise forms.ValidationError(errors["has requested"])

        except(AlreadyInvited):
            raise forms.ValidationError(errors["already_invited"])
        except(AlreadyAccepted):
            raise forms.ValidationError(errors["already_accepted"])
        except(UserRegisteredEmail):
            raise forms.ValidationError(errors["email_in_use"])

        return email

class PasswordRecoveryForm(forms.Form):
    username_or_email = forms.CharField()

    error_messages = {
        'not_found': _("Sorry, this user doesn't exist."),
    }

    def __init__(self, *args, **kwargs):
        self.case_sensitive = kwargs.pop('case_sensitive', True)
        search_fields = kwargs.pop('search_fields', ('username', 'email'))
        super(PasswordRecoveryForm, self).__init__(*args, **kwargs)

        message = ("No other fields than username and email are supported "
                   "by default")
        if len(search_fields) not in (1, 2):
            raise ValueError(message)
        for field in search_fields:
            if field not in ['username', 'email']:
                raise ValueError(message)

        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'both': _('Username or Email'),
        }
        User = get_user_model()  # noqa
        if getattr(User, 'USERNAME_FIELD', 'username') == 'email':
            self.label_key = 'email'
        elif len(search_fields) == 1:
            self.label_key = search_fields[0]
        else:
            self.label_key = 'both'
        self.fields['username_or_email'].label = labels[self.label_key]

    def clean_username_or_email(self):
        username = self.cleaned_data['username_or_email']
        cleaner = getattr(self, 'get_user_by_%s' % self.label_key)
        self.cleaned_data['user'] = user = cleaner(username)

        user_is_active = getattr(user, 'is_active', True)
        recovery_only_active_users = getattr(settings,
                                             'RECOVER_ONLY_ACTIVE_USERS',
                                             False)

        if recovery_only_active_users and not user_is_active:
            raise forms.ValidationError(_("Sorry, inactive users can't "
                                        "recover their password."))

        return username

    def get_user_by_username(self, username):
        key = 'username__%sexact' % ('' if self.case_sensitive else 'i')
        User = get_user_model()
        try:
            user = User._default_manager.get(**{key: username})
        except User.DoesNotExist:
            raise forms.ValidationError(self.error_messages['not_found'],
                                        code='not_found')
        return user

    def get_user_by_email(self, email):
        validate_email(email)
        key = 'email__%sexact' % ('' if self.case_sensitive else 'i')
        User = get_user_model()
        try:
            user = User._default_manager.get(**{key: email})
        except User.DoesNotExist:
            raise forms.ValidationError(self.error_messages['not_found'],
                                        code='not_found')
        return user

    def get_user_by_both(self, username):
        key = '__%sexact'
        key = key % '' if self.case_sensitive else key % 'i'

        def f(field):
            return Q(**{field + key: username})
        filters = f('username') | f('email')
        User = get_user_model()
        try:
            user = User._default_manager.get(filters)
        except User.DoesNotExist:
            raise forms.ValidationError(self.error_messages['not_found'],
                                        code='not_found')
        except User.MultipleObjectsReturned:
            raise forms.ValidationError(_("Unable to find user."))

        return user


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_('New password (confirm)'),
        widget=forms.PasswordInput,
    )

    error_messages = {
        'password_mismatch': _("The two passwords didn't match."),
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data['password2']
        if not password1 == password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password1'])
        if commit:
            get_user_model()._default_manager.filter(pk=self.user.pk).update(
                password=self.user.password,
            )
        return self.user