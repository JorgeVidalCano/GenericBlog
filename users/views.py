from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.views.generic import DeleteView, View
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse

from Mailchimp.models import Signup
from users.models import Profile
from blog.models import Post

class MyLoginView(LoginView):
    # Adds functionality to Remember_me in the login
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        if not self.request.POST.get('remember_me', None):
            self.request.session.set_expiry(0)
        
        login(self.request, form.get_user())

        return HttpResponseRedirect(self.get_success_url())

class DeleteAccount(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name='users/deleteAccount.html'
    success_url = "/"
    
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'Deleting'
        return context

    def test_func(self):
        # Overriden func. Checks that the user is the author
        object = self.get_object()
        if self.request.user == object:
            return True
        return False


def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST, label_suffix='')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            form.save()
            messages.success(request, f'Welcome to our community {username}.')
            user = authenticate(
                username = username,
                password = password
            )
            login(request, user)
            return redirect('blog-home')
        else:
            for m, e in form.errors.as_data().items():
                errorMessage = str(e[0]).replace("['", "").replace("']", "")
            messages.error(request, errorMessage)
    else:
        form = UserRegisterForm(label_suffix='')
    if request.user.is_authenticated:
        return redirect('profile')
        
    context = {
        "form": form,
        "titleTab": "Profile",
    }
    return render(request, 'users/register.html', context)

@login_required
def profile(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user, label_suffix='')
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile, label_suffix='')
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!.')
            return redirect('profile')
        else: 
            for m, e in u_form.errors.as_data().items():
                errorMessage = str(e[0]).replace("['", "").replace("']", "")
                messages.error(request, errorMessage)
    else:
        u_form = UserUpdateForm(instance=request.user, label_suffix='')
        p_form = ProfileUpdateForm(instance=request.user.profile, label_suffix='')        
        user_profile = Profile.objects.get(user=request.user)

    context = {
        "u_form": u_form,
        "p_form": p_form,
        "favoritePosts": user_profile.favoritePosts.all(),
        "titleTab": "Profile"
    }
    return render(request, 'users/profile.html', context)

def removeFav(request, slug):
    instance = {}
    
    if request.method == 'POST':
        profile = Profile.objects.get(user= request.user)
        
        try:
            post = get_object_or_404(Post, slug= slug)
            profile = Profile.objects.get(user=request.user)
        
            profile.addRemoveFav(request.user, post, True)

            return JsonResponse({"instance": slug}, status=200)
        except Exception as e:
            return JsonResponse({"instance": "Something happened"}, status=400)

    return render(request, 'users/profile.html')
