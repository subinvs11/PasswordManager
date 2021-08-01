from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import SignUpView, CustomAuthToken, OrganizationView, PersonalPasswordViewSet, \
    OrganizationPasswordViewSet

app_name = 'user_management'
router = DefaultRouter()
router.register('personal-password', viewset=PersonalPasswordViewSet, basename='personal_password_crud')
router.register('organization-password', viewset=OrganizationPasswordViewSet, basename='organization_password_crud')

urlpatterns = [
    path('', include(router.urls)),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('create-organization/', OrganizationView.as_view(), name='create_organization'),
    path('update-organization/<int:pk>/', OrganizationView.as_view(), name='update_organization'),
]