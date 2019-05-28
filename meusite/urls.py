from django.contrib import admin
from django.urls import path, include
# from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('blog.urls')),
	path('accounts/', include('accounts.urls')),
	path('accounts/login/', views.LoginView.as_view(), name='login'),
	path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
	path('accounts/', include('django.contrib.auth.urls'))
]

# Url de arquivos staticos em modo de debug
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
