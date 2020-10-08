from django.urls import path
from comments.views import CommentView


urlpatterns = [
    path('add', CommentView.as_view(), name="add-comment"),
    path('<int:pkComment>/update', CommentView.as_view(), name="update-comment"),
    path('<int:pkComment>/remove', CommentView.as_view(), name="remove-comment"),
    # path('<int:pkComment>/update', CommentRequest, name="update-comment"),
    # path('<int:pkComment>/remove', CommentRequest, name="remove-comment"),
    # path('<int:com>/update', UpdateComment.as_view(), name="update-comment"),
    # path('<int:com>/remove', CommentView.as_view(), name="remove-comment"),
]