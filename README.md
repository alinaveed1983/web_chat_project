# web_chat_project
Full stack project 2: Web Chat Application project built using Django, HTML, CSS, and JavaScript.

# WorkFlow
The workflow of the below project tree is divided into authentication, chat room functionality, and the interaction between the frontend and backend. Below is the step-by-step explanation of how the different components work together.


![image](https://github.com/user-attachments/assets/f539bb59-6929-4a4a-b757-790eaf1e23f2)

# Authentication Workflow
### User Registration
  ##### Frontend:
  1. The user accesses the `register.html` form from the `accounts_app` app.
  2. They input details like username, email, and password.

  ##### Backend:
  1. The form data is processed in the `accounts_app/views.py` using Django's `UserCreationForm` or a custom form in `forms.py`.
  2. If valid, a new user is created in the database and redirected to the login page.

  ##### Database:
  1. A new user record is added to the `User` model in the database.

### Login/Logout
  ##### Login:
  1. The user submits credentials via `login.html` handled by Django's auth views in `accounts_app/views.py`.
  2. On successful authentication, the user is redirected to the homepage (`index.html` in `chat_app`).

  ##### Logout:
  1. The user clicks a logout link that routes to the Django logout view.
  2. After logout, the user is redirected to the login page.



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



