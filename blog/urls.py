from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('post/new/', views.post_new, name='post_new'),
	path('post/<int:pk>', views.post_detail, name='post_detail'),
	path('author/<str:author_name>', views.posts_author, name='posts_author'),
	path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
	path('home/', TemplateView.as_view(template_name='blog/index.html')),
	path('sobre/', TemplateView.as_view(template_name='blog/sobre.html')),
]
