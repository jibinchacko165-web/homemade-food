"""
fix_images.py
-------------
Links existing images in media/food_images/ to the correct FoodItem records.
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

# Map: food item name  →  image filename (inside media/food_images/)
IMAGE_MAP = {
    'Idli & Sambar':            None,                          # no matching image
    'Masala Dosa':              'masala_dosa_1777994299938.png',
    'Puttu & Kadala Curry':     'puttu_kadala_curry.png',
    'Appam & Stew':             'appam_veg_stew.png',
    'Kerala Sadhya Plate':      'kerala_sadhya_1777992202421.png',
    'Fish Curry & Rice':        'kappa_meen_curry_kerala.png',
    'Chicken Biriyani':         'pathiri_chicken_curry_kerala.png',
    'Vegetable Stew & Appam':   'appam_veg_stew.png',
    'Banana Chips':             None,
    'Unniyappam':               'unniyappam_1777992220847.png',
    'Pazham Pori':              'pazham_pori_1777994333096.png',
    'Samosa (2 pcs)':           None,
    'Beef Ularthiyathu':        'kerala_parotta_beef_roast.png',
    'Prawn Moilee':             'karimeen_pollichathu_1777994315764.png',
    'Palak Paneer & Roti':      None,
    'Egg Roast & Porotta':      'porotta_beef_1777992236415.png',
}

updated = 0
skipped = 0
not_found = 0

for name, img_file in IMAGE_MAP.items():
    try:
        item = FoodItem.objects.get(name=name)
    except FoodItem.DoesNotExist:
        print(f"  [MISS]  FoodItem not in DB: '{name}'")
        not_found += 1
        continue

    if img_file is None:
        print(f"  [SKIP]  No image mapped for: '{name}'")
        skipped += 1
        continue

    # The ImageField path is relative to MEDIA_ROOT
    relative_path = f'food_images/{img_file}'
    item.image = relative_path
    item.save(update_fields=['image'])
    print(f"  [OK]    '{name}'  →  {relative_path}")
    updated += 1

print()
print(f"Done! Updated: {updated} | Skipped (no image): {skipped} | Not in DB: {not_found}")
