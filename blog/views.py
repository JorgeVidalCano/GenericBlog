from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from users.models import Profile
from django.core import serializers
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from .forms import PostCreateForm, PostPublishForm
from comments.forms import NewCommentForm
from TagPost.forms import TagCreateForm
from TagPost.models import TagPost
from ConfigBlog.models import ConfigBlog, AboutFields
from .models import Post, LikeCounter
from django.views.generic import(
     ListView, 
     DetailView, 
     CreateView,
     UpdateView,
     DeleteView,
     RedirectView,
     TemplateView
    )
from django.views import View

from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator
import re
import json
import datetime
#from comments.models import CommentPost

class HomeView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'Home'

        self.isTimeToPublish()

        filters ={"publish": True}
        if self.kwargs.get("slug"): 
            # If tag filter is used
            tag = TagPost.objects.get(slug=self.kwargs.get("slug"))          
            filters["tags"] = tag
            context['title'] = tag.tag.title
        else:
            # All posts
            context['title'] = 'All Posts'
        
        posts = Post.objects.filter(**filters).order_by('-date_posted')[:5]

        context['posts'] = posts
        return context
    
    def isTimeToPublish(self):
        # Publish posts that have been programmed
        posts = Post.objects.filter(publish=False)
        
        for p in posts:
            p.publicate()

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['date_posted']
    template_name = "blog/listPosts.html"
    form_model = PostPublishForm

    def get_queryset(self):
        ordering = ['date_posted']
        return Post.objects.filter(author=self.request.user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'My posts'
        context['username'] = self.request.user
        context['fields'] = ['Title', 'Comments', 'Likes', 'Dislikes', 'Slug', 'Posted date', 'Publish']
        context['imgUser'] = self.request.user.profile.profileImage.url
        context['form'] = self.form_model()
        return context

    def post(self, *args, **kwargs):

        if self.request.is_ajax() and self.request.method == "POST":
                    
            form = self.form_model(self.request.POST)
            if form.is_valid():
                post = Post.objects.get(slug= self.request.POST['slugPost'])

                #I dont get why I could not do it in a proper way :S
                if str(self.request.POST['publishPost']) == "False": 
                    post.publish = True
                else:
                    post.publish = False

                post.save(update_fields= ['publish'])
                
                return JsonResponse({"instance": f"<strong>{post.title}</strong> has been "}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)

            return JsonResponse({"error": self}, status=400)
            
class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "superuser"
    model = Post
    form_class = PostCreateForm

    template_name = "blog/create_post.html"

    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        # adds new data
        context['titleTab'] = 'New post'
        context['titlePage'] = 'New post'
        return context
    
    def form_valid(self, form):
        # Adds the author to the post
        form.instance.author = self.request.user
        super().form_valid(form)
        selectedTags = TagPost.objects.filter(pk__in=self.request.POST.getlist('tags'))
        form.instance.tags.set(selectedTags)
        
        # only access if some pic is uploaded
        if bool(self.request.FILES):
            form.instance.PostImages = self.request.FILES['postImage']
        form.instance.slug = self.slugifier(self.request.POST['title'])
        return super().form_valid(form)

    def slugifier(self, title):
        # I know I couldve used slugigy
        # Converts the title to slug
        self.slug = re.sub('\s+', '-', title)
        if self.slug[-1] == '-':
            self.slug = self.slug[:-1]
        
        if self.slug[0] == '-':
            self.slug = self.slug[1:]

        return self.slug

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = "blog/create_post.html"

    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        # adds new
        slug = self.kwargs.get("slug")
        context['titleTab'] = 'Updating ' + slug.replace('-', ' ').title()
        post = Post.objects.get(slug= slug)
        context['titlePage'] = 'Updating ' + slug.replace('-', ' ').title()
        context['hideTagIds'] = post.tags
        return context

    def test_func(self):
        # Overriden func. Checks that the user is the author
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    def form_valid(self, form):
        # Adds the author to the post
        form.instance.author = self.request.user
        selectedTags = TagPost.objects.filter(pk__in=self.request.POST.getlist('tags'))
        if selectedTags.count() != 0:
            form.instance.tags.set(selectedTags)

        # only access if some pic is uploaded
        if bool(self.request.FILES):
            form.instance.PostImages = self.request.FILES['postImage']
        form.instance.slug = self.slugifier(self.request.POST['title'])
        return super().form_valid(form)

    def slugifier(self, title):
        # Converts the title to slug
        self.slug = re.sub('\s+', '-', title)
        if self.slug[-1] == '-':
            self.slug = self.slug[:-1]
        
        if self.slug[0] == '-':
            self.slug = self.slug[1:]

        return self.slug

class PostDetailView(DetailView):
    model = Post
    form_model = NewCommentForm
    template_name = "blog/detail_post.html"
    context_object_name = 'post' 

    def get(self, *args, **kwargs):
        form = self.form_model()
        slug = self.kwargs.get("slug")
        post = Post.objects.get(slug= slug)
        comments = post.comments.all().order_by("-comment_date")

        try:
            profile = Profile.objects.get(user= self.request.user)
            favorite = profile.isFavorite(post, self.request.user)
        except Exception as AnonymousUser:
            favorite = False, False

        self.context = {
            'titleTab': slug.replace("-", " ").title(),
            'post': post,
            'form': form,
            'comments': comments,
            'showFavButton': True, # Always shown in details
            'isFavorite': favorite,
            'meta': post.meta
        }
        
        return render(self.request, self.template_name, self.context)

    # def post(self, *args, **kwargs):
    #     if self.request.is_ajax() and self.request.method == "POST":
            
    #         form = self.form_model(self.request.POST)
    #         if form.is_valid():
                
    #             # save the comment
    #             form.instance.authorComment = self.request.user.profile
    #             form.instance.comment = self.request.POST['comment']
    #             instance = form.save()
                
    #             # Adds comment to post
    #             slug = self.kwargs.get("slug")
    #             post = Post.objects.get(slug= slug)
    #             post.comments.add(instance.pk)
                
    #             ser_instance = serializers.serialize('json', [ instance, ])
    #             ## Gets the users name and the img
    #             username = self.request.user.username
    #             profileImg = Profile.objects.get(user=self.request.user).profileImage.url
    #             # # send to client side.
    #             return JsonResponse({"instance": ser_instance, "name":username.title(), "img": profileImg}, status=200)
    #         else:
    #             return JsonResponse({"error": form.errors}, status=400)

    #         return JsonResponse({"error": self}, status=400)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"
    context_object_name = 'post' 
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'Deleting'
        return context

    def test_func(self):
        # Overriden func. Checks that the user is the author
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@method_decorator(csrf_exempt, name="dispatch")
class PostLikeRedirect(RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        
        user = self.request.user        

        if not user.is_authenticated:
            return 
        if self.request.is_ajax() and self.request.method == "POST":
            
            slug = self.kwargs.get("slug")
            post = get_object_or_404(Post, slug= slug)
            value = self.request.POST["value"]
            
            opinion = LikeCounter()
            opinion.addLike(post, user, value)            

        return post.get_absolute_url()

@method_decorator(csrf_exempt, name="dispatch")
class PostFavoriteRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        
        user = self.request.user
        if not user.is_authenticated:
            return 
        if self.request.is_ajax() and self.request.method == "POST":
            
            slug = self.kwargs.get("slug")
            post = get_object_or_404(Post, slug= slug)
            
            profile = Profile.objects.get(user=user)
            isFavorite = self.request.POST["value"]
            profile.addRemoveFav(user, post, isFavorite)
            
        return post.get_absolute_url()

class AboutView(View):
    
    def get(self, request):
        about = AboutFields.objects.all()
        context = {
            "titleTab": "About me",
            "title": "About me",
            "about": about
        }
        return render(request, "blog/about.html", context)

