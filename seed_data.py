"""
Seed script: creates admin, chef, and sample menu items in TiDB Cloud.
Run: python seed_data.py
"""
import os
import sys
import django

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_system.settings')
django.setup()

from customers.models import CustomUser
from chef.models import FoodItem, ChefProfile

# --- 1. Admin ----------------------------------------------------------------
admin, created = CustomUser.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@homemadefood.com',
        'role': 'admin',
        'is_staff': True,
        'is_superuser': True,
        'first_name': 'Super',
        'last_name': 'Admin',
    }
)
if created:
    admin.set_password('Admin@1234')
    admin.save()
    print("[OK] Admin created  ->  username: admin | password: Admin@1234")
else:
    print("[--] Admin already exists")

# --- 2. Chef -----------------------------------------------------------------
chef, created = CustomUser.objects.get_or_create(
    username='chef_mary',
    defaults={
        'email': 'mary@homemadefood.com',
        'role': 'chef',
        'first_name': 'Mary',
        'last_name': 'Thomas',
        'phone_number': '9876543210',
    }
)
if created:
    chef.set_password('Chef@1234')
    chef.save()
    print("[OK] Chef created   ->  username: chef_mary | password: Chef@1234")
else:
    print("[--] Chef already exists")

# Chef profile
ChefProfile.objects.get_or_create(
    chef=chef,
    defaults={
        'bio': 'Passionate home cook specialising in Kerala and South Indian cuisine.',
        'specialty': 'Kerala Cuisine',
        'years_of_experience': 8,
        'is_verified': True,
    }
)

# --- 3. Menu Items -----------------------------------------------------------
menu = [
    # Breakfast
    dict(name='Idli & Sambar',         category='Breakfast', price=60,  prep=20, desc='Soft steamed rice cakes served with tangy sambar and coconut chutney.'),
    dict(name='Masala Dosa',            category='Breakfast', price=80,  prep=25, desc='Crispy crepe filled with spiced potato masala, served with chutney.'),
    dict(name='Puttu & Kadala Curry',   category='Breakfast', price=70,  prep=30, desc='Steamed rice cylinders with hearty black chickpea curry.'),
    dict(name='Appam & Stew',           category='Breakfast', price=90,  prep=35, desc='Lacy rice hoppers served with aromatic vegetable or chicken stew.'),
    # Lunch
    dict(name='Kerala Sadhya Plate',    category='Lunch',     price=180, prep=45, desc='Traditional banana-leaf feast with rice, sambar, avial, and payasam.'),
    dict(name='Fish Curry & Rice',      category='Lunch',     price=150, prep=40, desc='Kerala-style spicy fish curry with steamed rice and pappadom.'),
    dict(name='Chicken Biriyani',       category='Lunch',     price=200, prep=60, desc='Fragrant Malabar-style chicken biriyani with raita and pickle.'),
    dict(name='Vegetable Stew & Appam', category='Lunch',     price=120, prep=35, desc='Mild coconut-milk vegetable stew paired with soft appam.'),
    # Snacks
    dict(name='Banana Chips',           category='Snacks',    price=40,  prep=15, desc='Crispy fried raw banana chips lightly salted with coconut oil.'),
    dict(name='Unniyappam',             category='Snacks',    price=50,  prep=20, desc='Small sweet rice-and-banana fritters, a Kerala tea-time favourite.'),
    dict(name='Pazham Pori',            category='Snacks',    price=45,  prep=15, desc='Golden batter-fried ripe banana fritters irresistibly sweet.'),
    dict(name='Samosa (2 pcs)',         category='Snacks',    price=40,  prep=20, desc='Crispy pastry pockets filled with spiced potatoes and peas.'),
    # Dinner
    dict(name='Beef Ularthiyathu',      category='Dinner',    price=180, prep=50, desc='Dry-roasted Kerala beef stir-fry with coconut and curry leaves.'),
    dict(name='Prawn Moilee',           category='Dinner',    price=220, prep=40, desc='Delicate prawn curry in light coconut milk, best with appam.'),
    dict(name='Palak Paneer & Roti',    category='Dinner',    price=140, prep=35, desc='Creamy spinach gravy with cottage cheese, served with whole-wheat roti.'),
    dict(name='Egg Roast & Porotta',    category='Dinner',    price=120, prep=30, desc='Spicy Kerala egg roast paired with flaky layered porotta.'),
]

created_count = 0
for item in menu:
    obj, created_item = FoodItem.objects.get_or_create(
        name=item['name'],
        chef=chef,
        defaults={
            'category': item['category'],
            'price': item['price'],
            'description': item['desc'],
            'preparation_time': item['prep'],
            'is_available': True,
        }
    )
    if created_item:
        created_count += 1

print(f"[OK] Menu items created: {created_count}/{len(menu)}")
print("")
print("-------------------------------------------------")
print("Seed complete! Login credentials:")
print("  Admin  ->  admin / Admin@1234")
print("  Chef   ->  chef_mary / Chef@1234")
print("-------------------------------------------------")


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_system.settings')
django.setup()

from customers.models import CustomUser
from chef.models import FoodItem, ChefProfile

# ─── 1. Admin ────────────────────────────────────────────────────────────────
admin, created = CustomUser.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@homemadefood.com',
        'role': 'admin',
        'is_staff': True,
        'is_superuser': True,
        'first_name': 'Super',
        'last_name': 'Admin',
    }
)
if created:
    admin.set_password('Admin@1234')
    admin.save()
    print("✅ Admin created  →  username: admin | password: Admin@1234")
else:
    print("ℹ️  Admin already exists")

# ─── 2. Chef ─────────────────────────────────────────────────────────────────
chef, created = CustomUser.objects.get_or_create(
    username='chef_mary',
    defaults={
        'email': 'mary@homemadefood.com',
        'role': 'chef',
        'first_name': 'Mary',
        'last_name': 'Thomas',
        'phone': '9876543210',
    }
)
if created:
    chef.set_password('Chef@1234')
    chef.save()
    print("✅ Chef created   →  username: chef_mary | password: Chef@1234")
else:
    print("ℹ️  Chef already exists")

# Chef profile
ChefProfile.objects.get_or_create(
    chef=chef,
    defaults={
        'bio': 'Passionate home cook specialising in Kerala and South Indian cuisine.',
        'specialty': 'Kerala Cuisine',
        'years_of_experience': 8,
        'is_verified': True,
    }
)

# ─── 3. Menu Items ───────────────────────────────────────────────────────────
menu = [
    # Breakfast
    dict(name='Idli & Sambar',        category='Breakfast', price=60,  prep=20, desc='Soft steamed rice cakes served with tangy sambar and coconut chutney.'),
    dict(name='Masala Dosa',           category='Breakfast', price=80,  prep=25, desc='Crispy crepe filled with spiced potato masala, served with chutney.'),
    dict(name='Puttu & Kadala Curry',  category='Breakfast', price=70,  prep=30, desc='Steamed rice cylinders with hearty black chickpea curry.'),
    dict(name='Appam & Stew',          category='Breakfast', price=90,  prep=35, desc='Lacy rice hoppers served with aromatic vegetable or chicken stew.'),
    # Lunch
    dict(name='Kerala Sadhya Plate',   category='Lunch',     price=180, prep=45, desc='Traditional banana-leaf feast with rice, sambar, avial, and payasam.'),
    dict(name='Fish Curry & Rice',     category='Lunch',     price=150, prep=40, desc='Kerala-style spicy fish curry with steamed rice and pappadom.'),
    dict(name='Chicken Biriyani',      category='Lunch',     price=200, prep=60, desc='Fragrant Malabar-style chicken biriyani with raita and pickle.'),
    dict(name='Vegetable Stew & Appam',category='Lunch',     price=120, prep=35, desc='Mild coconut-milk vegetable stew paired with soft appam.'),
    # Snacks
    dict(name='Banana Chips',          category='Snacks',    price=40,  prep=15, desc='Crispy fried raw banana chips lightly salted with coconut oil.'),
    dict(name='Unniyappam',            category='Snacks',    price=50,  prep=20, desc='Small sweet rice-and-banana fritters, a Kerala tea-time favourite.'),
    dict(name='Pazham Pori',           category='Snacks',    price=45,  prep=15, desc='Golden batter-fried ripe banana fritters — irresistibly sweet.'),
    dict(name='Samosa (2 pcs)',        category='Snacks',    price=40,  prep=20, desc='Crispy pastry pockets filled with spiced potatoes and peas.'),
    # Dinner
    dict(name='Beef Ularthiyathu',     category='Dinner',    price=180, prep=50, desc='Dry-roasted Kerala beef stir-fry with coconut and curry leaves.'),
    dict(name='Prawn Moilee',          category='Dinner',    price=220, prep=40, desc='Delicate prawn curry in light coconut milk, best with appam.'),
    dict(name='Palak Paneer & Roti',   category='Dinner',    price=140, prep=35, desc='Creamy spinach gravy with cottage cheese, served with whole-wheat roti.'),
    dict(name='Egg Roast & Porotta',   category='Dinner',    price=120, prep=30, desc='Spicy Kerala egg roast paired with flaky layered porotta.'),
]

created_count = 0
for item in menu:
    obj, created_item = FoodItem.objects.get_or_create(
        name=item['name'],
        chef=chef,
        defaults={
            'category': item['category'],
            'price': item['price'],
            'description': item['desc'],
            'preparation_time': item['prep'],
            'is_available': True,
        }
    )
    if created_item:
        created_count += 1

print(f"✅ Menu items created: {created_count}/{len(menu)}")

print("\n─────────────────────────────────────────")
print("🎉  Seed complete! Login credentials:")
print("   Admin  →  admin / Admin@1234")
print("   Chef   →  chef_mary / Chef@1234")
print("─────────────────────────────────────────")
