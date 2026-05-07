"""
add_missing_foods.py — adds missing food items and links all images
"""
import os, sys, django
sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_system.settings')
django.setup()

from chef.models import FoodItem

# Use the same chef as existing items
chef = FoodItem.objects.first().chef
print("Chef:", chef.username)

missing = [
    {
        'name': 'Banana Chips',
        'category': 'Snacks',
        'price': 40,
        'description': 'Crispy Kerala banana chips fried in coconut oil. A classic tea-time snack.',
        'image': 'food_images/banana_chips_gen.png',
    },
    {
        'name': 'Palak Paneer & Roti',
        'category': 'Dinner',
        'price': 160,
        'description': 'Creamy spinach gravy with soft paneer cubes served with whole wheat rotis.',
        'image': 'food_images/palak_paneer_roti_gen.png',
    },
    {
        'name': 'Egg Roast & Porotta',
        'category': 'Dinner',
        'price': 120,
        'description': 'Spicy egg masala roast with flaky Kerala porotta. A beloved street food combo.',
        'image': 'food_images/egg_roast_porotta_gen.png',
    },
]

for m in missing:
    obj, created = FoodItem.objects.get_or_create(
        name=m['name'],
        defaults=dict(
            chef=chef,
            category=m['category'],
            price=m['price'],
            description=m['description'],
            image=m['image'],
            is_available=True,
        )
    )
    if not created:
        obj.image = m['image']
        obj.save(update_fields=['image'])
    status = "CREATED" if created else "UPDATED"
    print(f"  [{status}] {obj.name}")

print()
print("All done! Total items:", FoodItem.objects.count())
