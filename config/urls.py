"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.shortcuts import redirect, render
from django.views.generic import RedirectView, TemplateView
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib.auth import logout as auth_logout
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from config import settings
from users.views import CustomTokenObtainPairView, LogoutJWTView


class JWTSchemaGenerator(OpenAPISchemaGenerator):
    def get_security_definitions(self):
        security_definitions = super().get_security_definitions()
        security_definitions["Bearer"] = {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
        return security_definitions


schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="SalesTGBot API",
        contact=openapi.Contact(email="yoldoshevfpydev@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=JWTSchemaGenerator,
)

def custom_logout_view(request):
    auth_logout(request)
    return redirect("/login/")

def auth_view(request):
    return render(request, "auth.html")

from django.contrib import admin



urlpatterns = [
    path('api/v1/', include('tgbot.urls')),
    path("admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path('auth/', auth_view, name="auth"),

    # Swagger va Redoc manzillari:
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/logout/', LogoutJWTView.as_view(), name='logout_jwt'),


    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico", permanent=True)),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Also serve legacy media/ folder (files uploaded before MEDIA_ROOT was changed to mediafiles/)
    import os

    legacy_media = os.path.join(settings.BASE_DIR, "media")
    if os.path.isdir(legacy_media):
        urlpatterns += static(settings.MEDIA_URL, document_root=legacy_media)
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()






def custom_page_not_found(request, exception):
    return render(request, "404.html", status=404)


def custom_server_error(request):
    return render(request, "500.html", status=500)


handler404 = custom_page_not_found
handler500 = custom_server_error