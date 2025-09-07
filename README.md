### **Pictale Project: A Comprehensive Guide**

Pictale is a full-stack photo-sharing project built on **Django**. It offers a complete solution with robust user authentication, a RESTful API, and a dynamic frontend.



### **🚀 Key Features**

  * **User Authentication**: Provides secure registration and login functionalities.
  * **RESTful API**: Uses **Django REST Framework** for user authentication and data management. Access is secured via token-based authentication.
  * **Dynamic Frontend**: A complete web interface built with Django templates, featuring:
      * **Home Page**: Displays a daily featured photo with a narrative story.
      * **User Profile**: Allows users to view and edit their profiles, including a picture and bio.
      * **User Interactions**: Users can like, save, and comment on photos.
      * **Photo Recommendations**: Users can submit their own photos for review.
      * **Responsive Design**: A modern, clean design that works on all devices.



### **🛠️ Installation & Setup**

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Emane11/Pictale_Project.git
    cd Pictale_Project
    ```
2.  **Create & activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate # On macOS/Linux
    venv\Scripts\activate # On Windows
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run migrations**:
    ```bash
    python manage.py migrate
    ```
5.  **Start the development server**:
    ```bash
    python manage.py runserver
    ```

The application will be accessible at **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**.



### **📡 API Endpoints**

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/auth/register/` | Register a new user |
| **POST** | `/api/auth/login/` | Log in a user |



### **🖥️ Frontend URLs**

| Endpoint | Description |
| :--- | :--- |
| `/` | Home page displaying the daily photo |
| `/profile/` | User profile page with saved photos |
| `/profile/edit/` | Page for editing user profile information |
| `/recommendations/` | Page to submit photo recommendations |
| `/login/` | User login page |
| `/register/` | User registration page |



### **🧪 Testing**

  * **API Testing**: Use **Postman** to import the provided collection (`postman_collection.json`) and send requests to **[http://127.0.0.1:8000/api/auth/](http://127.0.0.1:8000/api/auth/)**.
  * **Frontend Testing**: Navigate to **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser to access the web application.



### **📂 Project Structure**

```
Pictale_Project/
├── pictale_app/        # Main app for frontend views, templates, and models
│   ├── templates/      # HTML templates for frontend rendering
│   ├── migrations/
│   ├── views/
│   ├── models.py
│   ├── urls.py
│   └── ...
├── Pictale_Project/    # Project settings
├── manage.py
└── requirements.txt
```



### **🤝 Contributing**

Pull requests are welcome. For major changes, please open an issue first to discuss the proposed changes.
