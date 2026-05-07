from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin-panel/', admin.site.urls),          # Django admin
    path('management/', include('management.urls')), # Custom admin dashboard
    path('', include('chef.urls')),                  # Food listing & chef dashboard
    path('customers/', include('customers.urls')),   # Customer auth
    path('orders/', include('orders.urls')),
]

# Serve media files in all environments (dev + production)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
