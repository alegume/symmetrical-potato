from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	path('post_list/', views.post_list, name='post_list'),
	path('', TemplateView.as_view(template_name='blog/index.html')),
	path('sobre/', TemplateView.as_view(template_name='blog/sobre.html')),
]
