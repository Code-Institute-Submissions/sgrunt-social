"""
Imports:
"""
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView


class PostListView(View):
    """
    Post feed view
    """
    def get(self, request, *args, **kwargs):
        """ Iterate through posts and display them from newest to last """
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }
        return render(request, 'core/post_list.html', context)

    def post(self, request, *args, **kwargs):
        """ Handles post request and saves the new post """
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
        
        context = {
            'post_list': posts,
            'form': form,
        }
        return render(request, 'core/post_list.html', context)


class PostDetailView(View):
    """ Post specific page view, with ability to comment and display all comments """
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'core/post_detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
        
        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'core/post_detail.html', context)


class PostEditView(UpdateView):
    """ Ability to edit a post """
    model = Post
    fields = ['body']
    template_name = 'core/post_edit.html'

    def get_success_url(self):
        """ redirect to post detail page when edit is successful """
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})


class PostDeleteView(DeleteView):
    """ Ability to delete post """
    model = Post
    template_name = 'core/post_delete.html'
    success_url = reverse_lazy('post-list')


class CommentDeleteView(DeleteView):
    """ Ability to delete comment """
    model = Comment
    template_name = 'core/comment_delete.html'

    def get_success_url(self):
        """ redirect to post detail page when delete is successful """
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})
