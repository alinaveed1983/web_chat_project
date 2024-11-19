# web_chat_project
Full stack project 2: Web Chat Application project built using Django, HTML, CSS, and JavaScript.

# WorkFlow
The workflow of the below project tree is divided into authentication, chat room functionality, and the interaction between the frontend and backend. Below is the step-by-step explanation of how the different components work together.


![image](https://github.com/user-attachments/assets/f539bb59-6929-4a4a-b757-790eaf1e23f2)

# Authentication Workflow
### User Registration
  #### Frontend:
  1. The user accesses the `register.html` form from the `accounts_app` app.
  2. They input details like username, email, and password.

  #### Backend:
  1. The form data is processed in the `accounts_app/views.py` using Django's `UserCreationForm` or a custom form in `forms.py`.
  2. If valid, a new user is created in the database and redirected to the login page.

  #### Database:
  1. A new user record is added to the `User` model in the database.

### Login/Logout
  #### Login:
  1. The user submits credentials via `login.html` handled by Django's auth views in `accounts_app/views.py`.
  2. On successful authentication, the user is redirected to the homepage (`index.html` in `chat_app`).

  #### Logout:
  1. The user clicks a logout link that routes to the Django logout view.
  2. After logout, the user is redirected to the login page.

