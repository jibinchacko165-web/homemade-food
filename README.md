# 🍱 Homemade Food Ordering System

A premium, time-aware food ordering platform designed for a seamless connection between home chefs and food enthusiasts. This system features a sophisticated time-based menu, distinct user roles (Chef, Customer, Admin), and a modern, responsive user interface.

## 🌟 Key Features

### 👨‍🍳 Chef Module
- **Kitchen Dashboard**: Manage your menu and track inventory at a glance.
- **Dynamic Menu Management**: Add, edit, or remove dishes with custom pricing and images.
- **Order Tracking**: Real-time monitoring of customer orders with status updates (Pending/Completed/Cancelled).
- **Automated Categories**: Dishes are intelligently sorted into Breakfast, Lunch, Snacks, and Dinner.

### 😋 Customer Module
- **Time-Aware Menu**: The home page dynamically displays available dishes based on the current time of day (IST).
- **Seamless Cart Experience**: Add multiple items, adjust quantities, and manage your cart before checkout.
- **Order History**: Keep track of your past cravings and order statuses.
- **Premium UI**: Vibrant, glassmorphic design inspired by traditional Kerala aesthetics.

### 🛡️ Administrative Panel
- **Comprehensive Dashboard**: High-level statistics on users, chefs, orders, and platform revenue.
- **User Management**: Activate/deactivate accounts and manage user roles (Customer/Chef/Admin).
- **Platform Control**: Global oversight of food availability and order fulfillment.

## 🛠️ Technology Stack
- **Backend**: Django 4.2.21 (Python)
- **Database**: SQLite (Development) / MySQL (Production Ready)
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design System), JavaScript
- **Icons**: Font Awesome 6.0
- **Typography**: Google Fonts (Inter, Outfit)

## 📁 Project Structure
```text
├── food_system/       # Core project configuration
├── chef/              # Menu and Chef management module
├── customers/         # User authentication and profiles module
├── orders/            # Cart and Order processing module
├── management/        # Custom Administrative dashboard module
├── templates/         # Global template system
├── static/            # CSS, JS, and Branding assets
└── media/             # Dynamic food photography and uploads
```

## 🔐 Security & Optimization
- **Role-Based Access Control (RBAC)**: Strict decorators ensure users only see what they are authorized to.
- **Timezone Awareness**: Accurate scheduling using `Asia/Kolkata` (IST) for meal availability.
- **Responsive Design**: Fully optimized for Desktop, Tablet, and Mobile viewing.

---
*Created with ❤️ for Homemade Food Lovers.*
