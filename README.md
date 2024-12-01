# web_chat_project
Full stack project 2: Web Chat Application project built using Django, HTML, CSS, and JavaScript.

# WorkFlow
The workflow of the below project tree is divided into authentication, chat room functionality, and the interaction between the frontend and backend. Below is the step-by-step explanation of how the different components work together.


# pre-requisites
```
sudo apt update && sudo apt upgrade -y
sudo apt install pkg-config libmysqlclient-dev -y
sudo apt install sqlite3 python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv nginx net-tools -y
git clone https://github.com/alinaveed1983/web_chat_project.git
cd ~/web_chat_project

python3 -m venv venv
source venv/bin/activate
pip install django-extensions Django channels daphne whitenoise
```

# commands
```
python manage.py check
python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic
python manage.py createsuperuser
sudo usermod -aG www-data ubuntu
groups ubuntu
exit
sudo chown -R ubuntu:www-data /home/ubuntu/
sudo chmod -R 755 /home/ubuntu/

ls -ld /home
ls -ld /home/ubuntu
ls -ld /home/ubuntu/web_chat_project



python manage.py shell

python manage.py runasgi
http://127.0.0.1:8000/admin
-- create users and chatrooms

python manage.py show_urls


# DB commands
python manage.py dbshell
sqlite> .tables
sqlite> SELECT * FROM chat_app_chatroom;
sqlite> SELECT * FROM chat_app_message;
sqlite> .schema chat_app_message;
sqlite> pragma table_info(chat_app_message);
```

# daphne
```
sudo vi /etc/systemd/system/daphne.service
[Unit]
Description=Daphne Service for Web Chat Project
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/web_chat_project
Environment="PATH=/home/ubuntu/web_chat_project/venv/bin"
ExecStart=/home/ubuntu/web_chat_project/venv/bin/python manage.py runasgi

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl enable daphne
sudo systemctl start daphne
sudo systemctl status daphne
sudo journalctl -u daphne.service -n 50 --no-pager
```

# nginx
```
### Nginx configuration for HTTPS
sudo vi /etc/nginx/sites-available/web_chat
server {
    listen 443 ssl;
    server_name ec2-34-229-193-126.compute-1.amazonaws.com;

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

    # Proxy requests to Daphne
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Proxy WebSocket connections
    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Serve static files
    location /static/ {
        alias /home/ubuntu/web_chat_project/staticfiles/;
        autoindex on; # Optional for debugging
    }
}

sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/web_chat /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx
sudo tail -n 50 /var/log/nginx/error.log

sudo ss -tuln | grep 443
sudo netstat -tuln | grep 443
curl -I https://ec2-34-229-193-126.compute-1.amazonaws.com
```

# Authentication Workflow
### User Registration
>> ##### Frontend:
>> 1. The user accesses the `register.html` form from the `accounts_app` app.
>> 2. They input details like username, email, and password.

>> #### Backend:
>> 1. The form data is processed in the `accounts_app/views.py` using Django's `UserCreationForm` or a custom form in `forms.py`.
>> 2. If valid, a new user is created in the database and redirected to the login page.

>> #### Database:
>> 1. A new user record is added to the `User` model in the database.

### Login/Logout
>> #### Login:
>> 1. The user submits credentials via `login.html` handled by Django's auth views in `accounts_app/views.py`.
>> 2. On successful authentication, the user is redirected to the homepage (`index.html` in `chat_app`).

>> #### Logout:
>> 1. The user clicks a logout link that routes to the Django logout view.
>> 2. After logout, the user is redirected to the login page.


# Chat Room Workflow
### Chat Room Listing
>> #### Frontend:
>> 1. The homepage (`index.html`) displays a list of available chat rooms using a Django template.

>> #### Backend:
>> 1. The `chat_app/views.py` fetches all chat rooms from the `ChatRoom` model and passes the data to the template.

>> #### Database:
>> 1. The `ChatRoom` model contains records for each chat room.

### Joining a Chat Room
>> #### Frontend:
>> 1. When a user clicks on a chat room, they are taken to `chat_room.html` via a route in `chat_app/urls.py`.
>> 2. WebSocket connections are established to enable real-time communication.

>> #### Backend:
>> 1. The `chat_app/consumers.py` handles WebSocket connections for the chat room.
>> 2. The WebSocket receives and broadcasts messages to all connected users in the room.

>> #### Database:
>> 1. Messages are saved in the `Message` model with details like sender, room, and timestamp.

### Real-Time Chat
>> #### Frontend:
>> 1. The `chat.js` script manages WebSocket connections and dynamically updates the chat interface when new messages are received.
>> 2. When a user sends a message, it is sent via WebSocket to the server.

>> #### Backend:
>> 1. The WebSocket consumer (`chat_app/consumers.py`) receives the message and broadcasts it to all other users in the same room.
>> 2. It also saves the message in the database for persistence.

>> #### Database:
>> 1. Each message is stored in the `Message` model, linked to the corresponding `ChatRoom` and user.


# Interaction Between Frontend and Backend
### Static and Dynamic Content
>> #### Static Files:
>> 1. CSS (chat.css, base.css) and JavaScript (chat.js, main.js) files handle the styling and dynamic interactions on the frontend.

>> #### Dynamic Content:
>> 1. Django templates (index.html, chat_room.html) are populated with data from the backend (e.g., list of chat rooms, messages).

>> #### WebSocket Workflow
>> 1. WebSocket connections are handled by ASGI (via web_chat/asgi.py) and Django Channels:
>> 2. Connection: When the user accesses a chat room, a WebSocket connection is established.
>> 3. Message Exchange: The WebSocket consumer listens for incoming messages and broadcasts them to all users in the room.
>> 4. Disconnection: When the user leaves, the WebSocket connection is closed.


# Middleware and Routing
### HTTP Requests
>> 1. Middleware processes incoming HTTP requests (e.g., login, logout, page rendering).
>> 2. Requests are routed via web_chat/urls.py to the respective app (accounts_app or chat_app).
>> 3. Views in the app handle the request, fetch data from the database, and render the appropriate template.
### WebSocket Requests
>> 1. WebSocket connections are routed through web_chat/asgi.py to the chat_app/consumers.py.
>> 2. Consumers handle WebSocket events (e.g., connect, disconnect, receive message).


# Database Workflow
### User Authentication
>> 1. User credentials are stored in the default User model or a custom model in accounts_app/models.py.
>> 2. Chat Rooms and Messages

### ChatRoom model:
>> 1. Stores the name and details of chat rooms.

### Message model:
>> 1. Stores the content, sender, and timestamp of each message.
>> 2. Messages are linked to a ChatRoom and a User.

# Deployment Workflow
### Static Files
>> 1. Collected and served via Nginx or the Django collectstatic command.
>> 2. Gunicorn and Nginx
>> 3. Gunicorn serves the Django application, and Nginx acts as a reverse proxy to handle HTTP/HTTPS requests and serve static files.

# Summary
>> 1. Users authenticate themselves via accounts_app.
>> 2. They browse or join chat rooms listed by chat_app.
>> 3. Real-time communication in chat rooms is handled via WebSocket connections using Django Channels.
>> 4. Data such as chat rooms and messages is persistently stored in the database.
>> 5. Frontend components (HTML/CSS/JS) interact with backend logic for a seamless user experience.


# Tech Stack

| Category                | Technology                      | Purpose                                  |
|-------------------------|----------------------------------|------------------------------------------|
| **Frontend**            | HTML, CSS, JavaScript          | Structure, styling, and interactivity    |
| **Backend**             | Django Framework (Python)      | Server-side logic and API handling       |
| **Real-time Communication** | WebSockets with Django Channels | Real-time chat functionality             |
| **Database**            | SQLite (or other databases)    | Storing user data, chat rooms, and messages |
| **Web Server**          | Daphene + Nginx               | Hosting Django application and reverse proxy |
| **Authentication**      | Django Authentication System   | User registration, login, and logout     |
| **Dependencies**        | Python Libraries (in `requirements.txt`) | Required libraries for project functionality |
| **Static Files Management** | Django Static Files         | Serving CSS, JavaScript, and images      |
