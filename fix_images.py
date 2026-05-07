"""
fix_images.py
-------------
Links AI-generated food images to FoodItem records in the database.
Run from the project root:
    python fix_images.py
"""
import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_system.settings')
django.setup()

from chef.models import FoodItem

# Map: food item name → image filename (inside media/food_images/)
IMAGE_MAP = {
    'Idli & Sambar':            'idli_sambar.png',
    'Masala Dosa':              'masala_dosa_gen.png',
    'Puttu & Kadala Curry':     'puttu_kadala_gen.png',
    'Appam & Stew':             'appam_stew_gen.png',
    'Kerala Sadhya Plate':      'kerala_sadhya_gen.png',
    'Fish Curry & Rice':        'fish_curry_rice_gen.png',
    'Chicken Biriyani':         'chicken_biriyani_gen.png',
    'Vegetable Stew & Appam':   'veg_stew_appam_gen.png',
    'Banana Chips':             'banana_chips_gen.png',
    'Unniyappam':               'unniyappam_gen.png',
    'Pazham Pori':              'pazham_pori_gen.png',
    'Samosa (2 pcs)':           'samosa_gen.png',
    'Beef Ularthiyathu':        'beef_ularthiyathu_gen.png',
    'Prawn Moilee':             'prawn_moilee_gen.png',
    'Palak Paneer & Roti':      'palak_paneer_roti_gen.png',
    'Egg Roast & Porotta':      'egg_roast_porotta_gen.png',
}

updated = 0
not_found = 0

for name, img_file in IMAGE_MAP.items():
    try:
        item = FoodItem.objects.get(name=name)
    except FoodItem.DoesNotExist:
        print(f"  [MISS]  Not in DB: '{name}'")
        not_found += 1
        continue

    relative_path = f'food_images/{img_file}'
    item.image = relative_path
    item.save(update_fields=['image'])
    print(f"  [OK]    '{name}'  →  {relative_path}")
    updated += 1

print()
print(f"Done! Updated: {updated}/16 | Not in DB: {not_found}")
