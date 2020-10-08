from django.contrib import admin
from blog.views import AboutView
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from users import views as user_views
from users.views import MyLoginView, DeleteAccount
from django.conf import settings
from django.conf.urls.static import static
from TagPost.views import TagManager
from Mailchimp.views import email_list_signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', MyLoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('deleteAccount/<int:pk>', DeleteAccount.as_view(), name='delete-account'),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('tags/',include('TagPost.urls')),
    path('search/', include('searchEngine.urls')),
    path('about/', AboutView.as_view(), name="blog-about"),
    path('subscribe/', email_list_signup, name="postMailChimp"),
    path('', include('blog.urls')),
    re_path('djga/', include('google_analytics.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)