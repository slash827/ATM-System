# Railway Deployment Guide

## Quick Deploy to Railway

### Simple Deployment (Recommended for Example Projects)
1. Use the simplified `Dockerfile.railway` 
2. Deploy directly to Railway - should work out of the box!

### Environment Configuration
Railway will automatically detect your Python app. Optional environment variables:

```bash
# Optional Railway Environment Variables
PORT=8000
PYTHONUNBUFFERED=1
```

### Docker Configuration

**Railway Dockerfile** (`Dockerfile.railway`): Simple and compatible
- Uses `python:3.11-slim` (widely available)
- Minimal configuration for maximum compatibility
- Perfect for example/demo projects

**Main Dockerfile**: More secure but complex
- Multi-stage build with security features
- Use this for production deployments

### Quick Start
```bash
# Option 1: Rename the simple Dockerfile
mv Dockerfile.railway Dockerfile
git add . && git commit -m "Use simple Railway Dockerfile"
git push

# Option 2: Configure Railway to use the Railway Dockerfile
# In Railway dashboard: Settings -> Build -> Dockerfile Path = "Dockerfile.railway"
```

### Testing
Once deployed, test these endpoints:
- **Root**: `https://your-app.railway.app/` 
- **Health**: `https://your-app.railway.app/health`
- **API Docs**: `https://your-app.railway.app/docs`
- **Balance Check**: `https://your-app.railway.app/accounts/12345/balance`
