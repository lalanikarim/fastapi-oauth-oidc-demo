"""FastAPI OAuth OpenID Connect application with Authlib."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from config import settings
import os

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

# Initialize OAuth client
oauth = OAuth()

# Register auth.usa.ismaili OAuth client with OpenID Connect
oauth.register(
    name='ismaili',
    client_id=settings.oauth_client_id,
    client_secret=settings.oauth_client_secret,
    authorize_url=settings.oauth_authorize_url,
    access_token_url=settings.oauth_token_url,
    userinfo_endpoint=settings.oauth_userinfo_url,
    jwks_uri=settings.oauth_jwks_url,
    client_kwargs={
        'scope': 'openid offline_access'
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
    return await oauth.ismaili.authorize_redirect(request, redirect_uri)


@app.get("/auth")
async def auth(request: Request):
    """Handle OAuth callback and token exchange."""
    try:
        token = await oauth.ismaili.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        # Store user info and token in session
        request.session['user'] = dict(user_info)
        request.session['token'] = token
        
        return RedirectResponse(url="/profile")
    except Exception as e:
        # In production, you'd want proper error handling
        return HTMLResponse(f"<h1>Authentication Error</h1><p>{str(e)}</p>")


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
