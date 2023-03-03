from django.contrib import admin
from django.urls import re_path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path(r'', include('CTP.urls')),
    re_path(r'admin/', admin.site.urls),
    re_path(r'accounts/', include('django.contrib.auth.urls'))
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
