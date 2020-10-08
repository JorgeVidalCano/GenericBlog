from SocialMedia.models import SocialMedia
from django import template
from django.template.loader import get_template

t = get_template('templates/socialMedia/socialMediabuttons.html')

## Allows django to load this data everytime without having to repeat the code
register = template.Library()
@register.inclusion_tag(t)
def socialMediaButtons():
    social = SocialMedia.objects.filter(publish=True)
    
    return {
        "social": social
    }