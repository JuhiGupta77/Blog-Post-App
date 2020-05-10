# its okay to have views underline in red or showing as error, things will run fine
from blog import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name='post_list'), # this regex is used for home-page (is also used in case user logs-out)
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^post/news/$', views.CreatePostView.as_view(), name='post_new'),  # for post create view;
    url(r'^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='post_edit'),  # for post update view
    url(r'^post/(?P<pk>\d+)/remove/$', views.PostDeleteView.as_view(), name='post_remove'),  # for post delete view
    url(r'^drafts/$', views.DraftListView.as_view(), name='post_draft_list'),  # for draft posts list view
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'), # post_publish function in views.py
]