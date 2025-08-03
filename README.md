## System Setup and Installation Guide (For Linux/WSL) If Need

### 1. System Dependency Installation

The following dependencies are required to compile and run Python projects that rely on system-level libraries. You only need to install them **once per machine**.

#### Install Required Packages:

```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
libffi-dev liblzma-dev
```

> **Note:** This step is essential only for fresh Linux/WSL environments. If these dependencies are already installed (from a previous project), you may skip this section.

---

#### 2. (Optional) Install Python 3.12.x from Source

If the required Python version (e.g., 3.12.3) is not available in your package manager, you can manually build it:

#### Download and Compile Python:

```bash
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tgz
sudo tar xzf Python-3.12.3.tgz
cd Python-3.12.3
sudo ./configure --enable-optimizations
sudo make -j$(nproc)
sudo make altinstall
```

> **Warning:** Use `make altinstall` (not `make install`) to avoid replacing the default system Python.

You now have Python 3.12.x installed as `python3.12`.

---

## 3. Project Setup Instructions

Once system dependencies and Python are set:

#### 3.1 Create a Virtual Environment and Install Project Requirements:

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
#### 3.2set the .env from example.env


You are now ready to start development or run the project.


## Project Run
step-1: sudo service redis-server start
step-2: python3 -m daphne bugtracker.asgi:application

## Swagger Docs
    `/docs/`

## API endpoints
#### User Registration  
**POST** `/api/v1/registration/`  
Create a new user account. Returns JWT access and refresh tokens on success.

#### User Login (Token Obtain)  
**POST** `/api/v1/token/`  
Authenticate user credentials and receive JWT access and refresh tokens.

#### Token Refresh  
**POST** `/api/v1/token/refresh/`  
Send a valid refresh token to get a new access token without re-authenticating.

#### 1. Project CRUD API
**URL:** `/api/v1/project/`  
**Methods:** `GET`, `POST`, `PATCH`, `DELETE`  
**Permissions:** Authenticated users only  

- **GET**  
  - Retrieve all projects, or a specific project by providing `project_id` as a query parameter.  
  - Example:  
    ```
    GET /api/v1/project/?project_id=1
    ```

- **POST**  
  - Create a new project. The authenticated user is set as the owner.  
  - Required JSON body parameters:  
    - `name` (string)  
    - `description` (string)

- **PATCH**  
  - Partially update a project using the `project_id` query parameter and the fields to update in the request body.  
  - Example:  
    ```
    PATCH /api/v1/project/?project_id=1
    Body: { "description": "Updated description" }
    ```

- **DELETE**  
  - Delete a project by its `project_id`.  
  - Example:  
    ```
    DELETE /api/v1/project/?project_id=1
    ```

---

#### 2. Bug CRUD API

**URL:** `/api/v1/bug/`  
**Methods:** `GET`, `POST`, `PATCH`, `DELETE`  
**Permissions:** Authenticated users only  

- **GET**  
  - Retrieve bugs, optionally filtered by `bug_id`, `project_id`, or `status`.  
  - Examples:  
    ```
    GET /api/v1/bug/?bug_id=5
    GET /api/v1/bug/?project_id=1&status=Open
    ```

- **POST**  
  - Create a new bug. The authenticated user is set as the creator.  
  - Required JSON body parameters:  
    - `title` (string)  
    - `description` (string)  
    - `status` (Open, In Progress, Resolved)  
    - `priority` (Low, Medium, High)  
    - `project` (project ID)

- **PATCH**  
  - Partially update a bug using the `bug_id` query parameter.

- **DELETE**  
  - Delete a bug by `bug_id`.

---

#### 3. Comment CRUD API

**URL:** `/api/v1/comment/`  
**Methods:** `GET`, `POST`, `PATCH`, `DELETE`  
**Permissions:** Authenticated users only  

- **GET**  
  - Retrieve all comments or filter by `comment_id`.

- **POST**  
  - Create a new comment. The authenticated user is set as the commenter.  
  - Required JSON body parameters:  
    - `bug` (bug ID)  
    - `message` (string)

- **PATCH**  
  - Partially update a comment using the `comment_id` query parameter.

- **DELETE**  
  - Delete a comment by `comment_id`.

---

#### 4. Assigned Bugs API

**URL:** `/api/v1/bugs/assigned/`  
**Method:** `GET`  
**Permissions:** Authenticated users only  

- Retrieve bugs assigned to the authenticated user, or specify a user by `user_id` query parameter.  



# how to test WebSocket events.
#### 1st: Connect a WebSocket client (e.g., websocat, browser console, Postman WebSocket tab) to the URL ws://<your-domain>/ws/bugtracker/<project_id>/?token=<your_jwt_access_token>.   When connecting to the WebSocket, you need to pass the JWT token as a query parameter (e.g., ?token=your_jwt_token) for authentication.

#### 2nd: Once connected, any bug created or updated (even through normal API calls) will automatically trigger notifications to all connected clients in that project’s WebSocket group.This works because the backend uses Django signals to listen for bug model changes and broadcasts events through WebSockets to all users connected to the project room.
#### 3rd: The commenter uses the normal API to create the comment. The backend signal detects the new comment and sends a WebSocket event. The bug creator and the assigned user, if connected with a valid JWT token via WebSocket, will receive the notification instantly.

#### 4th: For testing the typing indicator event via Postman (WebSocket tab), you just send this JSON message in the message box: Once sent, the backend will broadcast this typing notification to other connected users in the same project room (except you).
---
{
  "type": "typing",
  "user": "Momenggg"
}


