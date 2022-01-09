from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from board.views import main
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
urlpatterns = [
    path('admin/', admin.site.urls),
    path('useraccount/', include('useraccount.urls')),
    path('user/', include('useraccount.urls')),
    path('board/', include('board.urls')),
    path('main/', main),
    path('summernote/', include('django_summernote.urls')),
    path('api/token/verify/', verify_jwt_token),
]
