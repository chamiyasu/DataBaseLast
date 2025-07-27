from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView
# )

urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('login/', views.LoginView.as_view()),
    # path('logout/', views.LogoutView.as_view()),
    # path('retry/', views.RetryView.as_view()),
    path('diary/', views.DiaryView.as_view()),
    # path('login/', views.LoginView.as_view()),
    path('diary/<int:id>/', views.DiaryView.as_view()),
    path('diary/<int:id>/edit', views.SaveView.as_view()),
    path('diary/add/', views.SaveView.as_view()),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)