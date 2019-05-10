from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


def home(request):
    context={
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html   blog/post_list.html
    # set an attribute. In def home, the loop was called 'posts' Either change in html from posts to objectlist or ser the context as below
    context_object_name = 'posts'
    #set an attribute for ordering. To see latest posts first. ['date_posted] from oldest to newest
    # [-date_posted] from newest to oldest
    ordering = ['-date_posted']
    paginate_by = 5
    # In class based views, we are setting varibales only. Then call the class as views in the urls.
    #However, in the function view,we had to render a function then pass info explicitly. 
    # if you would have used the generic, i mean, the names the list was looking for, like object_list intstead of posts, you would have saved some lines of code.
    # we would have had only the model = post line only.


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post  
    #<app>/<model>_<viewtype>.html -- the naming convention it is going to look for
    # This time we do not have the attribute context coz in out template, we called all post as object which the list was expecting.

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post  
    # in this case, it doesn't expect this format <app>/<model>_<viewtype>.html however it expects post_form.html
    fields = ['title','content']

    def form_valid(self, form):
        # we override the create validation to tell it this is the author of the post. Otherwise we'll get an integrity error
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post  
    # in this case, it doesn't expect this format <app>/<model>_<viewtype>.html however it expects post_form.html
    fields = ['title','content']

    def form_valid(self, form):
        # we override the create validation to tell it this is the author of the post. Otherwise we'll get an integrity error
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()  #get exact post we are updating. This is a method of the update view.
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  #the mixins have to be on the left of the view inheritance.
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()  #get exact post we are updating. This is a method of the update view.
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})