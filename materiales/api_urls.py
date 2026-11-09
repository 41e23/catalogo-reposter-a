from rest_framework.routers import SimpleRouter

from .api_views import MaterialViewSet

router = SimpleRouter()
router.register(r'materiales', MaterialViewSet, basename='api-materiales')

urlpatterns = router.urls
