from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('post/<int:pk>', views.post_detail, name='post_detail'),
	path('home/', TemplateView.as_view(template_name='blog/index.html')),
	path('sobre/', TemplateView.as_view(template_name='blog/sobre.html')),
]
