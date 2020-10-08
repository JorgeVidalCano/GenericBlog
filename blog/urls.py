from django.urls import path, include
from blog.views import (
    HomeView, PostListView, PostLikeRedirect, PostFavoriteRedirect, 
    PostCreateView, PostUpdateView, PostDetailView, PostDeleteView
)

from users.views import removeFav


urlpatterns = [
    path('<slug:slug>/', HomeView.as_view(), name="post-filter"),
    path('', HomeView.as_view(), name="blog-home"),
    path('post/myposts/', PostListView.as_view(), name="my-posts"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('post/<slug:slug>/comment/', include(("comments.urls","comments"))),
    path('post/<slug:slug>/like', PostLikeRedirect.as_view(), name="likes"),
    path('post/<slug:slug>/favorite', PostFavoriteRedirect.as_view(), name="favorite"),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('post/<slug:slug>/', PostDetailView.as_view(), name="post-detail"),
    path('profile/<slug:slug>/favorite', removeFav, name="rem-fav"),
    # path('about/', AboutView.as_view(), name="blog-about"),
]