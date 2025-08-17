# Pictale Project

Pictale is a Django-based project that provides authentication and API endpoints for user registration and login.  
This repository contains the source code and setup instructions.

---

## 🚀 Features
- User registration (`/api/auth/register/`)
- User login (`/api/auth/login/`)
- Token-based authentication
- Django REST Framework integration

---

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Emane11/Pictale_Project.git
   cd Pictale_Project
Create & activate a virtual environment

bash:
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
Install dependencies

bash:
pip install -r requirements.txt
Run migrations

bash:
python manage.py migrate
Start the development server

bash:
python manage.py runserver

📡 API Endpoints
Method	Endpoint	Description
POST	/api/auth/register/	Register new user
POST	/api/auth/login/	Login user

🧪 Testing with Postman
Open Postman.

Import the collection (postman_collection.json) if available.

Send a request to the API running at:
http://127.0.0.1:8000/api/auth/

📂 Project Structure

Pictale_Project/
├── api/                # App containing authentication logic
├── Pictale_Project/    # Project settings
├── manage.py
└── requirements.txt

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.