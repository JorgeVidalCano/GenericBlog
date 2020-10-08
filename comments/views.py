from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DeleteView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core import serializers
from users.models import Profile
from blog.models import Post
from .forms import NewCommentForm
from .models import CommentPost

class CommentView(DetailView):

    form_model = NewCommentForm

    def post(self, p, slug, pkComment=None, *args, **kwargs):
        # Without the p I got too many arguments for slug :S
        if self.request.is_ajax() and self.request.method == "POST":
            action = self.request.path.split("/")[-1]
            
            comment = CommentPost.objects.filter(pk=pkComment)
            
            if action == "update":
                newComment = self.request.POST['comment']
                comment.update(comment=newComment)
                return JsonResponse({"instance": newComment}, status=200)
            elif action == "remove":
                CommentPost.objects.get(pk=pkComment)
                comment.delete()
                return JsonResponse({"instance": "delete"}, status=200)
            else:
                form = self.form_model(self.request.POST)
                if form.is_valid():    
                    # Saves the comment
                    form.instance.authorComment = self.request.user.profile
                    form.instance.comment = self.request.POST['comment']
                    instance = form.save()
                    
                    # Adds comment to post
                    slug = self.kwargs.get("slug")
                    post = Post.objects.get(slug= slug)
                    post.comments.add(instance.pk)
                    
                    ser_instance = serializers.serialize('json', [ instance, ])
                    ## Gets the users name and the img
                    username = self.request.user.username
                    profileImg = Profile.objects.get(user=self.request.user).profileImage.url
                    # # send to client side.
                    return JsonResponse({"instance": ser_instance, "name":username.title(), "img": profileImg}, status=200)
                else:
                    return JsonResponse({"error": form.errors}, status=400)

                return JsonResponse({"error": self}, status=400)