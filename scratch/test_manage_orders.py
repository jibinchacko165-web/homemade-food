import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_system.settings')
django.setup()

from django.test import RequestFactory
from management.views import manage_orders
from customers.models import CustomUser

# Create a test request
factory = RequestFactory()
request = factory.get('/management/orders/')

# Get the admin user
admin_user = CustomUser.objects.get(username='admin')
request.user = admin_user

from django.contrib.messages.storage.fallback import FallbackStorage
setattr(request, 'session', 'session')
messages = FallbackStorage(request)
setattr(request, '_messages', messages)

try:
    response = manage_orders(request)
    print("Response Status Code:", response.status_code)
except Exception as e:
    print("Exception during view execution:", e)
    import traceback
    traceback.print_exc()
