from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import permissions
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import re_path

schema_view = get_schema_view(
   openapi.Info(
      title="Bug Tracker API",
      default_version='v1',
      description="API documentation for Bug Tracker project",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('apps.tracker.urls')),
    path('api/v1/', include('apps.user.urls')),    


    # Swagger UI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]

print(settings.DEBUG)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)