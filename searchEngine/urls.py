from django.urls import path, re_path
from searchEngine.views import SearchView , AjaxSearchView, AjaxPostList
from users.views import removeFav

urlpatterns = [
    path('', SearchView.as_view(), name='search-results'),
    path('ajaxCall/<int:page>', AjaxPostList.as_view(), name='load-more-posts'),
    path('ajaxCall/<int:page>/<tag>', AjaxPostList.as_view(), name='load-more-posts'), #re_path, why it didnt work    
    path('ajaxSearch/', AjaxSearchView.as_view(), name='ajaxSearch'),
]