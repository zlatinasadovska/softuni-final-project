from django.urls import path
from Echo.accounts import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
]
