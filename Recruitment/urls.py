from django.contrib import admin
from django.views.i18n import JavaScriptCatalog
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(r"jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path(r"", include("Evaluator.urls")),
    path(r"admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
