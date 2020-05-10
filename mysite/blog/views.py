from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
# By using common brackets we can write import statement in 2 lines
from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)

from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    ''' Django creates default_template i.e. model_form.html (adding _form.html after model name)
        i.e. post_form.html when ListView is used; use form variable to represent form in html file '''
    model = Post

    # predefined function for ListView
    def get_queryset(self):
        # an - in front of the published_date makes the get query to order it by "descending order"
        # __lte is less than equal to, please refer django documentation
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    ''' Django creates default_template i.e. model_form.html (adding _form.html after model name)
        i.e. post_form.html when DetailView is used; use form variable to represent form in html file '''
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    ''' Mixins i.e. LoginRequiredMixin are like decorators and are imp so that only logged-in users can create posts '''
    ''' decorators i.e. @loginrequired works only with function based views '''
    ''' We'll mix in the FBVs decorators with the classes thats how it gets it name mixin '''
    ''' first 2 fields i.e. login_url and redirect_field_name are specific to LoginRequiredMixin '''
    ''' form_class and model fields are specific to CreateView '''
    ''' Django creates default_template i.e. model_form.html (adding _form.html after model name) 
        i.e. post_form.html when CreateView is used; use form variable to represent form in html file '''
    login_url = '/login/'
    redirect_field_name = "blog/post_detail.html"
    form_class = PostForm  # form class to instantiate (i.e. represent); comes from forms.py
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    ''' Django creates default_template i.e. model_form.html (adding _form.html after model name)
        i.e. post_form.html when UpdateView is used; use form variable to represent form in html file '''
    login_url = '/login/'
    redirect_field_name = "blog/post_detail.html"
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    ''' DraftListView in order to save drafts which are yet not published '''
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        ''' Draft posts have to have a null published date and are ordered by created_date '''
        ''' Drafts posts will also be listed by PostListView with published posts '''
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


####################################################################################################
#  Useful Funtions
####################################################################################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()  # publish method from Post's model
    return redirect('post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk) # ---> 1111
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post # ---> 1111 new post's title i.e. obtained from post object is added to comment's post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve() # publish method from Comment's model
    # redirect to the post_detail.html having the primary_key of the post to which that comment was linked to
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # need to save post's pk i.e. post_pk value as by the time it gets deleted, we saved it in a variable and
    # used it after wards to keep a track of it
    post_pk = comment.post.pk
    comment.delete()
    # post_pk usage
    return redirect('post_detail', pk=post_pk)



