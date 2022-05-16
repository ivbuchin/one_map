from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tutorial.views import AboutUsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("users/", include("users.urls", namespace='users')),
    path("forum/", include("forum.urls", namespace='forum')),
    path("followers/", include("followers.urls", namespace='followers')),
    path("about_us/", AboutUsView.as_view(), name="about_us"),
    path("", include("tutorial.urls", namespace='tutorial')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
