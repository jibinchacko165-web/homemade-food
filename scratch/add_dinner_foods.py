import os
import django
import sys

# Add project root to sys.path
sys.path.append(os.getcwd())

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_system.settings')
django.setup()

from chef.models import FoodItem
from customers.models import CustomUser

def add_malayalam_dinner_foods():
    # Find a chef to assign the foods to
    chef = CustomUser.objects.filter(role='chef').first()
    if not chef:
        chef = CustomUser.objects.create_user(
            username='kerala_chef',
            password='password123',
            email='chef@example.com',
            role='chef'
        )
        print(f"Created new chef: {chef.username}")
    else:
        print(f"Using existing chef: {chef.username}")

    dinner_foods = [
        {
            'name': 'Kerala Parotta with Beef Roast',
            'malayalam_name': 'കേരള പൊറോട്ടയും ബീഫ് റോസ്റ്റും',
            'description': 'Flaky, layered flatbread served with spicy and slow-cooked beef roast with coconut slivers.',
            'price': 180.00,
            'category': 'Dinner',
            'preparation_time': 25
        },
        {
            'name': 'Appam with Vegetable Stew',
            'malayalam_name': 'അപ്പവും വെജിറ്റബിൾ സ്റ്റൂവും',
            'description': 'Soft and lacy rice pancakes served with a mild, creamy coconut milk-based vegetable stew.',
            'price': 120.00,
            'category': 'Dinner',
            'preparation_time': 20
        },
        {
            'name': 'Idiyappam with Egg Curry',
            'malayalam_name': 'ഇടിയപ്പവും മുട്ട കറിയും',
            'description': 'String hoppers made from rice flour served with a flavorful Kerala style egg curry.',
            'price': 100.00,
            'category': 'Dinner',
            'preparation_time': 15
        },
        {
            'name': 'Puttu and Kadala Curry',
            'malayalam_name': 'പുട്ടും കടല കറിയും',
            'description': 'Steamed cylinders of ground rice and coconut served with spicy black chickpeas curry.',
            'price': 90.00,
            'category': 'Dinner',
            'preparation_time': 20
        },
        {
            'name': 'Pathiri with Chicken Curry',
            'malayalam_name': 'പത്തിരിയും ചിക്കൻ കറിയും',
            'description': 'Thin rice pancakes served with traditional Malabar style chicken curry.',
            'price': 160.00,
            'category': 'Dinner',
            'preparation_time': 30
        },
        {
            'name': 'Kanji and Vanpayar Mezhukkupuratti',
            'malayalam_name': 'കഞ്ഞിയും വൻപയർ മെഴുക്കുപുരട്ടിയും',
            'description': 'Traditional rice gruel served with sautéed red cowpeas, papad, and pickle. The ultimate comfort food.',
            'price': 80.00,
            'category': 'Dinner',
            'preparation_time': 25
        },
        {
            'name': 'Kappa with Meen Curry',
            'malayalam_name': 'കപ്പയും മീൻ കറിയും',
            'description': 'Boiled and mashed tapioca seasoned with coconut and spices, served with spicy red fish curry.',
            'price': 150.00,
            'category': 'Dinner',
            'preparation_time': 35
        }
    ]

    for food_data in dinner_foods:
        # We'll prepend the Malayalam name to the description
        full_description = f"[{food_data['malayalam_name']}] {food_data['description']}"
        
        food, created = FoodItem.objects.update_or_create(
            name=food_data['name'],
            chef=chef,
            defaults={
                'description': full_description,
                'price': food_data['price'],
                'category': 'Dinner',
                'preparation_time': food_data['preparation_time'],
                'is_available': True
            }
        )
        if created:
            print(f"Added: {food.name}")
        else:
            print(f"Updated: {food.name}")

if __name__ == '__main__':
    add_malayalam_dinner_foods()
