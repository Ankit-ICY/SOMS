from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import RegisterViewSet, LoginViewSet,GoogleLoginView,MyInfoAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from company.views import CompanyViewSet
from django.conf import settings
from django.conf.urls.static import static
from staff.views import CompanyStaffViewSet

router = DefaultRouter()
router.register('auth/register', RegisterViewSet, basename='register')
router.register('companies', CompanyViewSet, basename='companies')
router.register('staff', CompanyStaffViewSet, basename='companystaff')
router.register('me', MyInfoAPIView, basename='myinfo')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login/', LoginViewSet.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/google/', GoogleLoginView.as_view(), name='google-login'),
    # path('api/user/me/', MyInfoAPIView, name='myinfo'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)