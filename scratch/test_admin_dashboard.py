import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_system.settings')
django.setup()

from django.test import RequestFactory
from management.views import admin_dashboard
from customers.models import CustomUser
from django.contrib.messages.storage.fallback import FallbackStorage

factory = RequestFactory()
request = factory.get('/management/dashboard/')
admin_user = CustomUser.objects.get(username='admin')
request.user = admin_user
setattr(request, 'session', 'session')
messages = FallbackStorage(request)
setattr(request, '_messages', messages)

try:
    response = admin_dashboard(request)
    print("Response Status Code:", response.status_code)
    print("Rendered successfully. Length:", len(response.content))
except Exception as e:
    print("Exception during view execution:", e)
    import traceback
    traceback.print_exc()
