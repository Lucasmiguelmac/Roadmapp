from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from account.views import registration_view, logout_view, login_view

urlpatterns = [

    path('admin/', admin.site.urls),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view.as_view(), name='login'),
    path('', include('roadmaps.urls')),
    
]

# Le agregamos un url a nuestras imágenes para poder ubicarlas en producción
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)