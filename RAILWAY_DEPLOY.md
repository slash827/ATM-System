# Railway Deployment Guide

## Quick Deploy to Railway

### 🚀 **FIXED: Port Variable Issue**

If you're getting `Error: '${PORT' is not a valid port number`, try these solutions:

#### **Solution 1: Use the Startup Script (Recommended)**
```toml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python start_server.py"
```

#### **Solution 2: Shell Command Wrapper**
```toml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "sh -c 'uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}'"
```

#### **Solution 3: Remove railway.toml (Let Railway Auto-detect)**
Delete the `railway.toml` file and let Railway automatically detect your Python app.

### Environment Configuration
Railway will automatically set:
- `PORT` - The port your app should listen on
- `RAILWAY_*` - Various Railway-specific variables

### Quick Start Steps
1. **Push your code** to GitHub
2. **Connect to Railway** 
3. **Choose one of the solutions above**
4. **Deploy!**

### Testing
Once deployed, test these endpoints:
- **Root**: `https://your-app.railway.app/` 
- **Health**: `https://your-app.railway.app/health`
- **API Docs**: `https://your-app.railway.app/docs`
- **Balance Check**: `https://your-app.railway.app/accounts/12345/balance`

### Troubleshooting

**Still getting port errors?**
- Delete `railway.toml` completely
- Railway will auto-detect your Python app
- Should work with default settings
