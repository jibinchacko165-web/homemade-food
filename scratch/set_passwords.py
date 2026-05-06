import os
import django
import sys

# Add project root to sys.path
sys.path.append(os.getcwd())

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_system.settings')
django.setup()

from customers.models import CustomUser

def set_passwords():
    # Set Admin
    admin_user, created = CustomUser.objects.get_or_create(username='admin')
    admin_user.set_password('admin')
    admin_user.role = 'admin'
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    if created:
        print("Created admin user with password 'admin'")
    else:
        print("Updated admin user password to 'admin'")

    # Set Chef
    chef_user, created = CustomUser.objects.get_or_create(username='chef')
    chef_user.set_password('chef')
    chef_user.role = 'chef'
    chef_user.is_staff = True
    chef_user.save()
    if created:
        print("Created chef user with password 'chef'")
    else:
        print("Updated chef user password to 'chef'")

if __name__ == '__main__':
    set_passwords()
