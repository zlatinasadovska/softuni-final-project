from django.urls import path
from Echo.common.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
