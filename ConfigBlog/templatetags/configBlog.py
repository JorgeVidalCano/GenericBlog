from ConfigBlog.models import ConfigBlog
from django import template
from django.template.loader import get_template

l = get_template('templates/configBlog/logo.html')
obj = ConfigBlog.objects.values()

## Allows django to load this data everytime without having to repeat the code
register = template.Library()
@register.inclusion_tag(l)
def logo():
    urlLogo = obj[0]["logo"]
    return {
        "brandLogo": urlLogo
    }

t = get_template('templates/configBlog/blogTitle.html')
@register.inclusion_tag(t)
def brandName():
    blogTitle = obj[0]["blogTitle"]
    return {
        "brandName": blogTitle
    }

f = get_template('templates/configBlog/footerContent.html')
@register.inclusion_tag(f)
def footerContent():
    footerTitle = obj[0]["footerTitle"]
    return {
        "footerContent": footerTitle
    }