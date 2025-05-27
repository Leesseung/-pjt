# backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views  import get_schema_view
from drf_yasg       import openapi
from rest_framework.routers import DefaultRouter
from finance.views import DailyPriceViewSet,CommodityPriceViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="금융상품 API 문서",
        default_version='v1',
        description="정기예금·적금 상품 조회 및 관리 API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter(trailing_slash=False)
router.register(r'prices', DailyPriceViewSet, basename='prices')
router.register(r'commodities/(?P<commodity>gold|silver)', CommodityPriceViewSet, basename='commodity-price')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/',include(router.urls)),


    # DRF 기본 토큰 발급 (no CSRF)
    path("api/v1/api-token-auth/", obtain_auth_token, name="api-token-auth"),

    # dj-rest-auth 로그인/로그아웃/유저조회
    path("api/v1/accounts/", include("dj_rest_auth.urls")),
    path("api/v1/accounts/registration/", include("dj_rest_auth.registration.urls")),

    # 커뮤니티 API
    path("api/v1/community/", include(("community.urls", "community"), namespace="community")),
    path('api/v1/accounts/', include('accounts.urls')),  # 프로필 엔드포인트 추가
    path('api/v1/accounts/', include('dj_rest_auth.urls')),

    # openai 챗봇 API
    path("api/v1/chat/", include("chat.urls")),
        # 2) Swagger UI (브라우저에서 보는 대화형 문서)
    path('swagger/',     schema_view.with_ui('swagger',  cache_timeout=0), name='schema-swagger-ui'),
    # 3) Redoc UI (선택)
    path('redoc/',       schema_view.with_ui('redoc',    cache_timeout=0), name='schema-redoc'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
