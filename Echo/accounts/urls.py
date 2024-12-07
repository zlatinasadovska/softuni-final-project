from django.urls import path
from Echo.accounts import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
