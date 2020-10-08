from django.template.loader import get_template
from django.contrib.auth.models import User
from Mailchimp.forms import EmailSignupForm
from Mailchimp.models import Signup
from django import template


s = get_template('templates/mailchimp/subscribe.html')

## Allows django to load this data everytime without having to repeat the code
register = template.Library()

@register.inclusion_tag(s, takes_context=True)
def subscribeNewsletter(context):
    email_signup_qs = Signup.objects.filter(email=context["user"].email)
    
    status = "Unsubscribre from newletter" if email_signup_qs.exists() else "Subscribe to newsletter"
    
    subscribeForm = EmailSignupForm
    
    return {
        "subscribeForm": subscribeForm,
        "subscription": status
    }

