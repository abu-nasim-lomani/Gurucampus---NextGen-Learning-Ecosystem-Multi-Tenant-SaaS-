# gurucampus/urls.py
from django.contrib import admin
from django.urls import path, include

# --- 1. Import these two for media files ---
from django.conf import settings
from django.conf.urls.static import static
# -------------------------------------------

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls), # Using standard quotes
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/", include("users.urls")),
    path("api/v1/", include("courses.urls")),
    path("api/v1/", include("tenants.urls")),
    path("api/v1/", include("assessments.urls")),
    path("api/v1/", include("academics.urls")),
    path("api/v1/", include("subscriptions.urls")),
    path("api/v1/", include("marketplace.urls")),
]

# --- 2. Add this block at the bottom ---
# This tells Django how to serve media files (like PDFs) in development mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)