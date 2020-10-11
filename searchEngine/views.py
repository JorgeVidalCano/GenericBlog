from django.template.defaultfilters import slugify
from django.views.generic import ListView
from django.http import JsonResponse
from blog.models import Post
from django.db.models import Q 
from django.core import serializers
from django.core.paginator import Paginator
from TagPost.models import TagPost
import datetime
import json


class SearchView(ListView):
    model = Post
    template_name = "blog/home.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        print("CONTEXT")
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'Home'

        context['title'] = f"Results for '{self.request.GET.get('q')}'"
        query = self.request.GET.get('q')
        post_list = Post.objects.filter( Q(title__icontains=query) & Q(publish=True) )
        context['posts'] = post_list
        return context

class AjaxSearchView(ListView):
    ''' It handles the ajax response'''
    model = Post

    def get(self, request, *args, **kwargs):

        if self.request.is_ajax() and self.request.method == "GET":
            
            query = self.request.GET.get('q')
            if query is None:
                return JsonResponse({"error": "No results"}, status=400)
            
            #post_list = Post.objects.filter( Q(title__icontains=query) & Q(publish=True) ).values("title", "slug", "PostImages__url")[:6]

            post_list = Post.objects.filter( Q(title__icontains=query) & Q(publish=True) )

            posts = []
            post = {}

            for p in post_list.object_list:
                post = {
                    "title": p.title.title(),
                    "image": p.PostImages.url,
                    "slug": p.slug,
                }
                
                posts.append(post)
            return posts

            instance = json.dumps(list(posts))
            print("INSTANCE", instance)
            return JsonResponse({"instance": instance}, status=200)

class AjaxPostList(ListView):
    #loads new post in the home
    def get(self, request, *args, **kwargs):
        
        
        if self.request.is_ajax() and self.request.method == "GET":
            filters = {"publish": True}
            if self.kwargs.get("tag") is not None:
                tag = TagPost.objects.get(slug=slugify(self.kwargs.get('tag')))
                filters["tags"] = tag

            try:
                self.post_list = Post.objects.filter(**filters).order_by('-date_posted')
                self.page = self.selectPostsByPage(self.post_list)
                ser_instance = self.getPosts(self.page)
                
                return JsonResponse({"instance": ser_instance, "end": False}, status=200)
            except Exception as ex:
                print(ex)
                return JsonResponse({"instance": None, "end": True}, status=200)    
    
    def selectPostsByPage(self, post_list):
        # we select the next 5 posts
        numberPage = self.kwargs.get("page")
        splitPag = Paginator(self.post_list, 5)
        self.page = splitPag.page(numberPage)
        
        return self.page
    
    def getPosts(self, page_post):
        # we get the 5 posts and serialize them
        posts = self.preserializer(page_post)
        ser_instance = json.dumps(list(posts))
        
        return ser_instance

    def preserializer(self, page_posts):
        # Because I was unable to retrieve the tags and author, I have to loop over through
        # the queryset and create a dict and add it to a list
        posts = []
        post = {}

        for p in page_posts.object_list:
            post = {
                "title": p.title.title(),
                "content": p.content,
                "image": p.PostImages.url,
                "datePosted": p.date_posted.strftime("%d-%b-%Y"),
                "author": p.author.username.title(),
                "slug": p.slug,
                "tags": [t.tag for t in p.findTags()]
            }
            
            posts.append(post)
        return posts

