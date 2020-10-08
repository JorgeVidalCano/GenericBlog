import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import EmailSignupForm
from .models import Signup
import hashlib

mailchimp = MailchimpMarketing.Client()
mailchimp.set_config({
"api_key": settings.MAILCHIMP_API_KEY,
"server": settings.MAILCHIMP_DATA_CENTER
})

list_id = settings.MAILCHIMP_EMAIL_LIST_ID

def member_info(email, status):

    member_info = {
        "status": status
    }
    if status == "subscribed":
        member_info.update({
            "email_address": email,
            "merge_fields": {
            "FNAME": "Add name",
            "LNAME": "Add surname"
            }
        })
    return member_info

def email_list_signup(request):

    form = EmailSignupForm(request.POST or None)
    if request.method == "POST":
        
        if form.is_valid():
            
            try:
                email_signup_qs = Signup.objects.filter(email=form.instance.email)
                if email_signup_qs.exists():
                    status = "unsubscribed"
                    member_email_hash = hashlib.md5(form.instance.email.encode('utf-8')).hexdigest()
                    response = mailchimp.lists.update_list_member(list_id, member_email_hash, member_info(form.instance.email, status))
                    contact = Signup.objects.get(email=form.instance.email)
                    contact.remove()
                    return JsonResponse({"instance": "You can always come back."}, status=200)
                else:
                    status = "subscribed"
                    response = mailchimp.lists.add_list_member(list_id, member_info(form.instance.email, status))
                    form.save() 
                    return JsonResponse({"instance": "You will receive the newsletter."}, status=200)
            except:
                
                return JsonResponse({"error": "Something went wrong, try it again later."}, status=400)
        return JsonResponse({"error": "Something went wrong, try it again later."}, status=400)
