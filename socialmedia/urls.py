from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #Django built-in admin panel.../admin
    path('admin/', admin.site.urls),
    #For /register, /login etc.
    path('', include('accounts.urls')),
    #For /feed/, /post/create/...
    path('', include('posts.urls')),
    #For /like/1/, /comment/1/, /follow/daniel/...
    path('', include('social.urls')),
    #For /inbox/, /messages/daniel/, /search/...
    path('', include('messaging.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)