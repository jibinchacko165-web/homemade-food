from pathlib import Path
import os
import sys
import django

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_system.settings')
django.setup()
from django.conf import settings

import cloudinary
import cloudinary.uploader

print("Testing Cloudinary Configuration...")
config_params = {
    'cloud_name': settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
    'api_key': settings.CLOUDINARY_STORAGE['API_KEY'],
    'api_secret': '1KBme3ZA0aXLq-FjYEH4-FWjbA', # Original guess
    'secure': True
}

def test_config(secret, label):
    print(f"\n--- Testing {label} ---")
    cloudinary.config(
        cloud_name=config_params['cloud_name'],
        api_key=config_params['api_key'],
        api_secret=secret,
        secure=True
    )
    try:
        result = cloudinary.uploader.upload(
            "https://cloudinary-devs.github.io/res.cloudinary.com/images/old_logo.png",
            folder="test_folder"
        )
        print(f"Success! URL: {result['secure_url']}")
        return True
    except Exception as e:
        print(f"Failed! Error: {e}")
        return False

# Test original
test_config('1KBme3ZA0aXLq-FjYEH4-FWjbA', 'Original')
# Test with leading dash (Secret-...)
test_config('-1KBme3ZA0aXLq-FjYEH4-FWjbA', 'Leading Dash')
# Test with O instead of 0
test_config('1KBme3ZAOaXLq-FjYEH4-FWjbA', 'O instead of 0')
