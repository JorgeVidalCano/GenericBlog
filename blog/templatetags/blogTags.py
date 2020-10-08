from TagPost.models import TagPost
from django import template
from django.template.loader import get_template

t = get_template('templates/shareblocks/sideTags.html')

## Allows django to load this data everytime without having to repeat the code
register = template.Library()
@register.inclusion_tag(t)
def PostTagLinks():
    tags = TagPost()
    tag = tags.allTags()
    
    return {
        "tags": tag
    }