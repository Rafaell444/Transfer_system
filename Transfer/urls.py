from django.conf import settings
from django.urls import path
from Transfer.views import upload_file, home, registration_view, login_view, logoutPage, DownloadFileView
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', upload_file, name='upload'),
    path('', home, name='home'),
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path("logout/", logoutPage, name="logout"),
    # path('download/<str:filename>/', download, name="download"),
    path('download/<int:pk>/', DownloadFileView.as_view(), name='download_file'),
]
