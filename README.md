# AWAS Backend - Applied Web Application Security

This is a deliberately insecure Flask backend application created for the Applied Web Application Security (AWAS) course project.

## Setup Instructions

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Navigate to the backend directory:

```bash
cd awas-backend
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Initialize the database with seed data:

```bash
python seed.py
```

This will create test users:

- **admin** / admin123 (admin role)
- **joel** / demo123 (user role)
- **samu** / demo123 (user role)
- **karri** / demo123 (user role)

5. Run the application:

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Authentication

- `POST /api/register` - Register new user
  - Body: `{username, email, password}`
- `POST /api/login` - Login user
  - Body: `{username, password}`
- `POST /api/logout` - Logout user

### Feed

- `GET /api/feed` - Get feed posts (supports ?search= parameter)
  - Header: `X-User-ID: <user_id>`
- `POST /api/feed` - Create new post
  - Body: `{user_id, title, text, private}`

### Admin

- `DELETE /api/admin/feed/delete` - Delete post
  - Body: `{post_id, user_id}`
- `DELETE /api/admin/user/delete` - Delete user
  - Body: `{user_id, current_user_id}`
- `POST /api/admin/user/promote` - Promote user to admin
  - Body: `{user_id, current_user_id}`
- `POST /api/admin/user/demote` - Demote user from admin
  - Body: `{user_id, current_user_id}`

## Intentional Vulnerabilities

This application contains the following vulnerabilities for educational purposes:

### 1. SQL Injection

- **Location**: `/api/login` and `/api/feed` endpoints
- **Issue**: User input is directly concatenated into SQL queries without sanitization
- **Exploitation**:
  - Login: `' OR '1'='1`
  - Search: `' OR 1=1 --`
- **Impact**: Attackers can bypass authentication or retrieve hidden posts

### 2. Username Enumeration

- **Location**: `/api/register` and `/api/login` endpoints
- **Issue**: Different error messages reveal whether a username exists
- **Exploitation**: Attackers can determine valid usernames by trying registration or login
- **Impact**: Reduces the username search space for brute force attacks

### 3. Weak Session Management

- **Location**: All endpoints
- **Issue**: Session token is simply the user_id; stored in localStorage on frontend
- **Exploitation**: Attackers can modify localStorage to impersonate any user
- **Impact**: Complete account hijacking without credential theft

### 4. Broken Access Control

- **Location**: Admin endpoints (`/api/admin/*`)
- **Issue**: No server-side role verification; relies entirely on frontend
- **Exploitation**: Any user can directly call admin endpoints by providing user_id
- **Impact**: Non-admin users can delete posts, delete users, and modify roles

### 5. Weak Cryptography

- **Location**: Password hashing
- **Issue**: Passwords are hashed with MD5 without salt
- **Exploitation**: MD5 is cryptographically broken; rainbow tables can recover passwords
- **Impact**: Compromised password database becomes easily cracked

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Posts Table

```sql
CREATE TABLE posts (
    post_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    private BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
```

## Default Test Credentials

To test the application, use these credentials:

- **Username**: `admin` / **Password**: `admin123` (admin user)
- **Username**: `joel` / **Password**: `demo123` (regular user)
- **Username**: `samu` / **Password**: `demo123` (regular user)
- **Username**: `karri` / **Password**: `demo123` (regular user)

## Frontend Integration

The React frontend at `../awas-frontend` is now configured to connect to this backend.

**Important**: Make sure both services are running:

1. Backend: `python app.py` (port 5000)
2. Frontend: `npm run dev` (typically port 5173)

The frontend will automatically make API calls to `http://localhost:5000/api` for all operations.

## Notes

- SQLite is used for simplicity and easy distribution
- CORS is enabled for local frontend development
- The application runs in debug mode for development
- All vulnerabilities are intentional for the security project
