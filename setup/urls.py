from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers, permissions
from cupons.views import ClienteViewSet, CuponsViewSet, ConsumoViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register('clientes', ClienteViewSet, basename='clientes')
router.register('cupons', CuponsViewSet, basename='cupons')
router.register('consumos', ConsumoViewSet, basename='consumos')

schema_view = get_schema_view(
    openapi.Info(
        title="Sua API",
        default_version='v1',
        description="API para o sistema de cupons de desconto",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('consumos/<str:cupom>', ConsumoViewSet.as_view({'get': 'listByCupom'}), name='consumos_by_cupom'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
