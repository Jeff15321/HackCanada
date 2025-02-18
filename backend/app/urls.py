from django.urls import path
from .views import (
    SignupView, LoginView, AllUsersView,
    NewProjectView, AllProjectsView, DeleteProjectView
)

urlpatterns = [
    # Auth endpoints
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/users/', AllUsersView.as_view(), name='all-users'),

    # Project endpoints
    path('projects/new/', NewProjectView.as_view(), name='new-project'),
    path('projects/all/', AllProjectsView.as_view(), name='all-projects'),
    path('projects/delete/', DeleteProjectView.as_view(), name='delete-project'),
] 