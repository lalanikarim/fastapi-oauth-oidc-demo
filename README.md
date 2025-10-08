# OAuth OpenID Connect Demo

A FastAPI application demonstrating OAuth 2.0 and OpenID Connect authentication using Authlib.

## Features

- ✅ OAuth 2.0 Authorization Code Flow
- ✅ OpenID Connect Integration
- ✅ Token Display (Access, Refresh, ID Token)
- ✅ User Profile Information
- ✅ Session Management
- ✅ Secure Logout
- ✅ Modern Bootstrap UI

## Prerequisites

- Python 3.13+
- uv (Python package manager)
- Google OAuth 2.0 Client ID and Secret

## Setup

1. **Clone and navigate to the project:**
   ```bash
   cd auth-test
   ```

2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and add your auth.usa.ismaili OAuth credentials:
   ```env
   SECRET_KEY=your-super-secret-key-here
   OAUTH_CLIENT_ID=your-ismaili-client-id
   OAUTH_CLIENT_SECRET=your-ismaili-client-secret
   ```

4. **Get auth.usa.ismaili OAuth Credentials:**
   - Contact the auth.usa.ismaili administrators to register your application
   - Provide them with the following information:
     - **Application Name**: FastAPI OAuth Demo App
     - **Redirect URI**: `http://localhost:8000/auth`
     - **Grant Types**: `authorization_code`
     - **Scopes**: `openid offline_access`
   - They will provide you with a Client ID and Client Secret

## Running the Application

```bash
uv run python main.py
```

Or using uvicorn directly:
```bash
uv run uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## Usage

1. Visit `http://localhost:8000`
2. Click "Login with Google"
3. Complete OAuth flow with Google
4. View your profile and tokens
5. Test logout functionality

## Project Structure

```
auth-test/
├── main.py              # FastAPI application
├── config.py            # Configuration management
├── pyproject.toml       # Dependencies and project config
├── templates/           # HTML templates
│   ├── base.html
│   ├── home.html
│   └── profile.html
├── env.example          # Environment variables template
└── README.md           # This file
```

## Technologies Used

- **FastAPI**: Modern, fast web framework
- **Authlib**: OAuth and OpenID Connect library
- **Jinja2**: Template engine
- **Bootstrap**: UI framework
- **Python 3.13**: Latest Python version
- **uv**: Fast Python package manager
