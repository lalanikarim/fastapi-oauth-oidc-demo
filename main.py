"""FastAPI OAuth OpenID Connect application with Authlib."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.httpx_client import AsyncOAuth2Client
from config import settings
import os
import time

# Initialize FastAPI app
app = FastAPI(
    title="OAuth OpenID Connect Demo",
    description="FastAPI application demonstrating OAuth OpenID Connect with Authlib",
    version="0.1.0",
    debug=settings.debug,
)

# Add session middleware (required for Authlib)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# Setup templates
templates = Jinja2Templates(directory="templates")

# Add custom filter for timestamp formatting
def format_timestamp(timestamp):
    """Format Unix timestamp to readable date."""
    if timestamp:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp)))
    return 'N/A'

templates.env.filters['format_timestamp'] = format_timestamp

# Initialize OAuth client
oauth = OAuth()

# Register OAuth client with OpenID Connect
if settings.oauth_discovery_url:
    # Use OpenID Connect Discovery (preferred method)
    oauth.register(
        name='oauth_client',
        client_id=settings.oauth_client_id,
        client_secret=settings.oauth_client_secret,
        server_metadata_url=settings.oauth_discovery_url,
        client_kwargs={
            'scope': settings.oauth_scopes
        }
    )
else:
    # Fallback to manual configuration
    oauth.register(
        name='oauth_client',
        client_id=settings.oauth_client_id,
        client_secret=settings.oauth_client_secret,
        authorize_url=settings.oauth_authorize_url,
        access_token_url=settings.oauth_token_url,
        userinfo_endpoint=settings.oauth_userinfo_url,
        jwks_uri=settings.oauth_jwks_url,
        client_kwargs={
            'scope': settings.oauth_scopes
        }
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with login option."""
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/login")
async def login(request: Request):
    """Initiate OAuth login flow."""
    redirect_uri = request.url_for('auth')
    return await oauth.oauth_client.authorize_redirect(request, redirect_uri)


@app.get("/auth")
async def auth(request: Request):
    """Handle OAuth callback and token exchange."""
    # Check for OAuth error parameters
    error = request.query_params.get('error')
    error_description = request.query_params.get('error_description')
    
    if error:
        # Handle OAuth provider errors
        troubleshooting = []
        
        if error == 'invalid_scope':
            troubleshooting = [
                "The requested OAuth scopes are not allowed for this client",
                "Contact your OAuth provider administrator to update client permissions",
                "Check that the requested scopes match your client configuration"
            ]
        elif error == 'access_denied':
            troubleshooting = [
                "You denied permission or cancelled the authorization request",
                "Try logging in again and grant all requested permissions",
                "Make sure you're using the correct account"
            ]
        elif error == 'invalid_client':
            troubleshooting = [
                "The OAuth client configuration is invalid",
                "Check that your client ID and secret are correct",
                "Verify the redirect URI matches your client configuration"
            ]
        else:
            troubleshooting = [
                "An unexpected error occurred during authentication",
                "Try logging in again in a few minutes",
                "Contact support if the problem persists"
            ]
        
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": f"OAuth authentication failed: {error}",
            "error_details": True,
            "error_code": error,
            "error_description": error_description,
            "troubleshooting": troubleshooting
        })
    
    try:
        token = await oauth.oauth_client.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        # Calculate token expiration time
        if 'expires_in' in token:
            token['expires_at'] = time.time() + token['expires_in']
        
        # Store user info and token in session
        request.session['user'] = dict(user_info)
        request.session['token'] = token
        
        return RedirectResponse(url="/profile")
    except Exception as e:
        # Handle unexpected errors
        troubleshooting = [
            "An unexpected error occurred during token exchange",
            "Check your internet connection and try again",
            "Contact support if the problem persists"
        ]
        
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": f"Token exchange failed: {str(e)}",
            "error_details": False,
            "troubleshooting": troubleshooting
        })


@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    """Display user profile and tokens."""
    user = request.session.get('user')
    token = request.session.get('token')
    
    if not user:
        return RedirectResponse(url="/login")
    
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user,
        "token": token
    })


@app.get("/logout")
async def logout(request: Request):
    """Logout and clear session."""
    request.session.clear()
    return RedirectResponse(url="/")


@app.get("/refresh")
async def refresh_token(request: Request):
    """Refresh access token using refresh token."""
    token = request.session.get('token')
    if not token or not token.get('refresh_token'):
        return HTMLResponse("<h1>Error</h1><p>No refresh token available. Please login again.</p>")
    
    try:
        # Create an OAuth2 client for token refresh
        client = AsyncOAuth2Client(
            client_id=settings.oauth_client_id,
            client_secret=settings.oauth_client_secret,
            token=token
        )
        
        # Refresh the token
        new_token = await client.refresh_token(
            settings.oauth_token_url,
            refresh_token=token['refresh_token']
        )
        
        # Calculate expires_at if expires_in is provided
        if 'expires_in' in new_token:
            new_token['expires_at'] = time.time() + new_token['expires_in']
        
        # Update session with new token
        request.session['token'] = new_token
        
        return RedirectResponse(url="/profile")
    except Exception as e:
        return HTMLResponse(f"<h1>Token Refresh Error</h1><p>{str(e)}</p><p>Please login again.</p>")


@app.get("/api/token-status")
async def token_status(request: Request):
    """API endpoint to check token status."""
    token = request.session.get('token')
    if not token:
        return {"authenticated": False, "message": "No token found"}
    
    # Check if token is expired (basic check)
    expires_at = token.get('expires_at')
    if expires_at and expires_at < time.time():
        return {
            "authenticated": False, 
            "expired": True, 
            "message": "Token expired",
            "has_refresh_token": bool(token.get('refresh_token'))
        }
    
    return {
        "authenticated": True,
        "expires_at": expires_at,
        "has_refresh_token": bool(token.get('refresh_token')),
        "token_type": token.get('token_type', 'Bearer')
    }


if __name__ == "__main__":
    import uvicorn
    
    # Validate settings before starting (skip for demo mode)
    try:
        settings.validate()
    except ValueError as e:
        print(f"⚠️  Configuration warning: {e}")
        print("🚀 Starting in demo mode - OAuth features will show setup instructions")
        print("   To enable OAuth, set up your Google credentials in a .env file")
        # Don't exit, just continue in demo mode
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
