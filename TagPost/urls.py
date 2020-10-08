from django.urls import path, include
from users import views as user_views

from TagPost.views import TagManager

urlpatterns = [
    path('', TagManager.as_view(), name='tag'),
    
]


