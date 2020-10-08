from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import RedirectView
from TagPost.models import TagPost
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from TagPost.forms import TagCreateForm
#from django.views import View


class TagManager(LoginRequiredMixin, CreateView):
    model = TagPost
    form_class = TagCreateForm

    template_name = "TagPost/managerTags.html"

    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        # adds new data
        context['titleTab'] = 'Tags'
        tags = TagPost()
        # Add in the tags
        context['tags'] = tags.allTags()
        return context
    
    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if form.is_valid():        
                instance = form.save()        
                ser_instance = serializers.serialize('json', [ instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            