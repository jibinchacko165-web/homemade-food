import os
import django
import sys
import shutil

# Add project root to sys.path
sys.path.append(os.getcwd())

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_system.settings')
django.setup()

from chef.models import FoodItem
from django.core.files import File

def update_dinner_foods_with_photos():
    # Mapping of food names to generated image files
    # Note: I need the exact filenames from the generation output
    image_dir = r"C:\Users\user\.gemini\antigravity\brain\fb6d2214-415b-427e-b7c5-e86c8324a1da"
    
    # I'll search for the most recent files matching the names
    image_map = {
        'Kerala Parotta with Beef Roast': 'kerala_parotta_beef_roast',
        'Appam with Vegetable Stew': 'appam_veg_stew',
        'Idiyappam with Egg Curry': 'idiyappam_egg_curry',
        'Puttu and Kadala Curry': 'puttu_kadala_curry',
        'Pathiri with Chicken Curry': 'pathiri_chicken_curry_kerala',
        'Kanji and Vanpayar Mezhukkupuratti': 'kanji_payar_traditional',
        'Kappa with Meen Curry': 'kappa_meen_curry_kerala'
    }

    all_files = os.listdir(image_dir)
    
    for food_name, img_prefix in image_map.items():
        # Find the file
        matching_files = [f for f in all_files if f.startswith(img_prefix) and f.endswith('.png')]
        if not matching_files:
            print(f"No image found for {food_name}")
            continue
            
        # Get the latest one
        img_file = sorted(matching_files)[-1]
        img_path = os.path.join(image_dir, img_file)
        
        try:
            food = FoodItem.objects.get(name=food_name)
            
            # Remove Malayalam caption from description
            # Description is like "[മലയാളം] English description"
            if food.description.startswith('['):
                parts = food.description.split(']', 1)
                if len(parts) > 1:
                    food.description = parts[1].strip()
            
            # Add the image
            with open(img_path, 'rb') as f:
                food.image.save(f"{img_prefix}.png", File(f), save=True)
            
            food.save()
            print(f"Updated {food_name} with photo and removed Malayalam caption.")
            
        except FoodItem.DoesNotExist:
            print(f"Food item {food_name} not found in DB.")
        except Exception as e:
            print(f"Error updating {food_name}: {e}")

if __name__ == '__main__':
    update_dinner_foods_with_photos()
