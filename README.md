# OAuth OpenID Connect Demo

FastAPI application implementing OAuth 2.0 and OpenID Connect authentication using Authlib. Supports any OAuth provider through configuration.

## Features

- OAuth 2.0 Authorization Code Flow
- OpenID Connect integration
- Token refresh functionality
- User profile display
- Session management
- Error handling for common OAuth scenarios
- Provider-agnostic configuration

## Prerequisites

- Python 3.13+
- uv (Python package manager)
- OAuth 2.0 Client ID and Secret from your provider

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
   
   Edit `.env` and add your OAuth provider credentials:
   ```env
   SECRET_KEY=your-super-secret-key-here
   OAUTH_CLIENT_ID=your-oauth-client-id
   OAUTH_CLIENT_SECRET=your-oauth-client-secret
   OAUTH_REDIRECT_URI=http://localhost:8000/auth
   OAUTH_SCOPES=openid offline_access
   OAUTH_AUTHORIZE_URL=https://your-provider.com/oauth2/auth
   OAUTH_TOKEN_URL=https://your-provider.com/oauth2/token
   OAUTH_USERINFO_URL=https://your-provider.com/userinfo
   OAUTH_JWKS_URL=https://your-provider.com/.well-known/jwks.json
   ```

4. **Get OAuth Provider Credentials:**
   - Contact your OAuth provider administrators to register your application
   - Provide them with the following information:
     - **Application Name**: FastAPI OAuth Demo App
     - **Redirect URI**: `http://localhost:8000/auth`
     - **Grant Types**: `authorization_code`
     - **Scopes**: `openid offline_access`
   - They will provide you with a Client ID and Client Secret
   - Update the provider URLs in your `.env` file with your provider's endpoints

## Running the Application

```bash
uv run python main.py
```

Or with uvicorn directly:
```bash
uv run uvicorn main:app --reload
```

The application runs on `http://localhost:8000`

## Usage

1. Navigate to `http://localhost:8000`
2. Click "Login with OAuth"
3. Complete OAuth flow with your provider
4. View profile and tokens
5. Use "Refresh Token" to get new access tokens
6. Click "Logout" to end session

## API Endpoints

- `GET /` - Homepage with login/logout options
- `GET /login` - Initiate OAuth login flow
- `GET /auth` - OAuth callback handler
- `GET /profile` - User profile and token display
- `GET /refresh` - Refresh access token
- `GET /logout` - End user session
- `GET /api/token-status` - Check token validity (JSON API)

## Project Structure

```
auth-test/
├── main.py                 # FastAPI application with OAuth routes
├── config.py               # Configuration and environment management
├── pyproject.toml          # Dependencies and project configuration
├── uv.lock                 # Dependency lock file for reproducible builds
├── env.example             # Environment variables template
├── .vscode/
│   └── launch.json         # VS Code debug configuration
├── templates/              # HTML templates
│   ├── base.html           # Base template with Bootstrap
│   ├── home.html           # Homepage with login/logout
│   ├── profile.html        # User profile and token display
│   └── error.html          # OAuth error handling page
├── docs/
│   └── plans/              # Project planning documents (gitignored)
└── README.md              # This file
```

## Technologies Used

- FastAPI
- Authlib
- Jinja2
- Bootstrap 5
- Python 3.13
- uv

## Error Handling

Handles common OAuth error scenarios:
- Invalid scope
- Access denied
- Invalid client
- Server errors

## Configuration

All provider-specific settings are configurable through environment variables. No hardcoded credentials.
