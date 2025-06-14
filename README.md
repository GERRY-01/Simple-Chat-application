# Simple Chat Application

A **real-time chat application** built with Django, Django Channels, and WebSockets.

## 🚀 Features
- User **registration & login**
- **Real-time messaging** using WebSockets
- User **profile picture support**
- WebSocket-based chat with **Daphne ASGI server**

## 📂 Project Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/GERRY-01/Simple-Chat-application
cd Simple-Chat-application

```

### 2️⃣ Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ 🔒 Setting Up the `.env` File
This project requires a **.env file** to store environment variables securely.
Inside the project root (where `manage.py` is located), create a new file named `.env` and add:
```
SECRET_KEY='your-secret-key'
DEBUG=True

DB_NAME='the name of your database'
DB_USER='the user of your database'
DB_PASSWORD='your database password'
DB_HOST='localhost'
``` 
### Note: To get the secret key you need to run the following commands in the terminal
```bash
python manage.py shell
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```
#### Use the command quit() to exit the shell

### 5️⃣ Handling the database
This project is set up to use **PostgreSQL** by default. If you're using a different database engine, update your `settings.py` file accordingly.
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # replace postgresql with your database engine
        'NAME':config('DB_NAME'),
        'USER':config('DB_USER'),
        'PASSWORD':config('DB_PASSWORD'),
        'HOST':config('DB_HOST'),
    }
}

```
If you're using MySQL, make sure you have `pip install mysqlclient` installed before running migrations

### 6️⃣ Apply Migrations
```bash
python manage.py migrate
```

### 7️⃣ Run the Server
```bash
daphne chatproject.asgi:application

```
### in your localhost go to the url http://localhost:8000/registration to register a new user and http://localhost:8000/login to login to the chat application if you already have an account