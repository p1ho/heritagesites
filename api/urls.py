from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import SimpleRouter
from rest_framework_swagger.views import get_swagger_view
from api.views import SiteViewSet

API_TITLE = 'heritagesites API'
API_DESC = 'A web API for creating, modifying and deleting Heritage Sites.'

docs_view = include_docs_urls(
    title=API_TITLE,
    description=API_DESC,
)

# Swagger view
schema_view = get_swagger_view(title = API_TITLE)

router = SimpleRouter()
router.register(r'sites', SiteViewSet, base_name='sites')
# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', docs_view),
    path('swagger-docs/', schema_view)
    # path('schema/', schema_view)
]
