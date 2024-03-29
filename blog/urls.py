from django.urls import path, include
from django.views.generic import TemplateView
from . import views

# from rest_framework import routers
#
# router = routers.DefaultRouter()
# router.register(r'rest_posts', views.rest_post_list, basename='Post')
# # router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>', views.post_detail, name='post_detail'),
    path('author/<str:author_name>', views.posts_author, name='posts_author'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('home/', TemplateView.as_view(template_name='blog/index.html')),
    path('sobre/', TemplateView.as_view(template_name='blog/sobre.html')),
    path('num_users/', views.num_users, name='num_users'),
    path('post/<pk>/opinion_up/', views.opinion_up, name='opinion_up'),
    path('post/<pk>/opinion_down/', views.opinion_down, name='opinion_down'),
    path('post/<pk>/love/', views.love, name='love'),
    # contato
    path('contato/', views.contato, name='contato'),
    path('contato/obg', views.obg, name='obg'),
    # Rest
    path('rest/posts/', views.rest_post_list, name='rest_post_list'),
    path('rest/post/<pk>/', views.rest_post_detail, name='rest_post_detail')
]
