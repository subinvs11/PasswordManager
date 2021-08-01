from django.urls import path, include

from api.views import SignUpView, CustomAuthToken, OrganizationView

app_name = 'user_management'

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('create-organization/', OrganizationView.as_view(), name='create_organization'),
    path('update-organization/<int:pk>/', OrganizationView.as_view(), name='update_organization'),
]