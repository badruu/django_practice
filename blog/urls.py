from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,UserPostListView
from . import views

urlpatterns = [
    path('',PostListView.as_view(), name='blog-home'),
    path('user/<str:username>',UserPostListView.as_view(), name='user-posts'),
    path('about/',views.about, name='blog-about'),
    path('post/<int:pk>/',PostDetailView.as_view(), name='post-detail'), # use the ability of django of adding variables to a route in a order make a route dynamic . ie post 1 as post/1 or post2 and post/2. Pk stands for primary key and for integers only.
    # why pk specifically. Coz thats what the DetailListView expects.
    path('post/new/',PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(), name='post-delete'),
]