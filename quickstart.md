# ⚡ Quick Start Guide

Follow these steps to get your Homemade Food Ordering System up and running in minutes.

## 📋 Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)

## 🛠️ Installation & Setup

### 1. Set Up Virtual Environment (Recommended)
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Initialize Database
Apply migrations to set up the database schema:
```powershell
python manage.py migrate
```

### 4. Create Administrative Account
Create a superuser to access both the Django Admin and the Custom Admin Panel:
```powershell
python manage.py createsuperuser
```

## 🚀 Running the Application

Start the development server:
```powershell
python manage.py runserver
```

Once the server is running, you can access the platform at:
- **Main Website**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Custom Admin Dashboard**: [http://127.0.0.1:8000/management/](http://127.0.0.1:8000/management/)
- **Django Admin Interface**: [http://127.0.0.1:8000/admin-panel/](http://127.0.0.1:8000/admin-panel/)

## 🧪 Testing Account Roles
To test different modules, create users with the following roles in the Admin Panel:
1. **Customer**: Can browse the menu and place orders.
2. **Chef**: Can access the "My Kitchen" dashboard and add food items.
3. **Admin**: Can access the "Admin Panel" for platform oversight.

---
**Note**: The menu visibility is time-dependent. If the menu appears empty, check the current IST time or add food items for the current category (Breakfast, Lunch, Snacks, or Dinner).
