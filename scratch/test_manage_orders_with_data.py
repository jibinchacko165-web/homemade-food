import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_system.settings')
django.setup()

from django.test import RequestFactory
from management.views import manage_orders
from customers.models import CustomUser
from orders.models import Order
from django.contrib.messages.storage.fallback import FallbackStorage

# Create a test request
factory = RequestFactory()
request = factory.get('/management/orders/')

# Get the admin user
admin_user = CustomUser.objects.get(username='admin')
request.user = admin_user
setattr(request, 'session', 'session')
messages = FallbackStorage(request)
setattr(request, '_messages', messages)

# Make sure there is at least one order
if not Order.objects.exists():
    print("No orders exist! Cannot fully test the template.")
else:
    print(f"Found {Order.objects.count()} orders.")

try:
    response = manage_orders(request)
    print("Response Status Code:", response.status_code)
    # Actually evaluate the template
    content = response.content
    print("Rendered successfully. Length:", len(content))
except Exception as e:
    print("Exception during view execution:", e)
    import traceback
    traceback.print_exc()
