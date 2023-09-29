from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from cupons.views import ClienteViewSet, CuponsViewSet, ConsumoViewSet

router = routers.DefaultRouter()
router.register('clientes', ClienteViewSet, basename='clientes')
router.register('cupons', CuponsViewSet, basename='cupons')
router.register('consumos', ConsumoViewSet, basename='consumos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('consumos/<str:cupom>', ConsumoViewSet.as_view({'get': 'listByCupom'}), name='consumos_by_cupom'),

]
