Pictale Project
Pictale is a Django-based project that provides a full-stack solution for photo sharing. It includes robust user authentication, a RESTful API, and a dynamic frontend for a seamless user experience.

🚀 Features
User Authentication: Secure registration and login functionalities.

API Endpoints: RESTful API for user authentication and data management using Django REST Framework.

Token-based Authentication: Ensures secure API access.

Dynamic Frontend: A complete web interface built with Django templates, offering the following features:

Home Page: Displays a daily featured photo with a narrative story.

User Profile: Allows users to view and edit their profile, including a profile picture and a bio.

User Interactions: Users can like, save, and comment on photos.

Photo Recommendations: Users can submit their own photo recommendations for review.

Responsive Design: The interface is styled for a modern, clean look that works across devices.

🛠️ Installation & Setup
Clone the repository

git clone [https://github.com/Emane11/Pictale_Project.git](https://github.com/Emane11/Pictale_Project.git)
cd Pictale_Project

Create & activate a virtual environment

python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

Install dependencies

pip install -r requirements.txt

Run migrations

python manage.py migrate

Start the development server

python manage.py runserver

The application will be accessible at http://127.0.0.1:8000/.

📡 API Endpoints
Method

Endpoint

Description

POST

/api/auth/register/

Register a new user

POST

/api/auth/login/

Log in a user

🖥️ Frontend URLs
Endpoint

Description

/

Home page displaying the daily photo

/profile/

User profile page with saved photos

/profile/edit/

Page for editing user profile information

/recommendations/

Page to submit photo recommendations

/login/

User login page

/register/

User registration page

🧪 Testing
API Testing with Postman:

Open Postman.

Import the provided collection (postman_collection.json) if available.

Send requests to the API running at http://127.0.0.1:8000/api/auth/.

Frontend Testing:

Access the web application by navigating to http://127.0.0.1:8000/ in your browser.

📂 Project Structure
Pictale_Project/
├── pictale_app/          # Main app for frontend views, templates, and models
│   ├── templates/        # HTML templates for frontend rendering
│   ├── migrations/
│   ├── views/
│   ├── models.py
│   ├── urls.py
│   └── ...
├── Pictale_Project/      # Project settings
├── manage.py
└── requirements.txt

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.