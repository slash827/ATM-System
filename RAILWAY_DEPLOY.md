# Railway Deployment Guide

## 🚀 **FIXED: Import and Port Errors**

If you're getting import errors or port issues, try these solutions in order:

### **Solution 1: Use Procfile (Simplest)**
Create a `Procfile` (already created):
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```
Then **delete** `railway.toml` and let Railway use the Procfile.

### **Solution 2: Use Railway-Specific Main File**
```toml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn main_railway:app --host 0.0.0.0 --port $PORT"
```

### **Solution 3: Use Original Main with Fixed Command**
```toml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

### **Solution 4: Auto-Detection**
Delete both `railway.toml` and `Procfile` - let Railway auto-detect everything.

## 🔧 **Troubleshooting Import Errors**

If you see import/module errors:
1. **Check requirements.txt** - make sure all dependencies are listed
2. **Use `main_railway.py`** - has better error handling and debugging
3. **Check Railway logs** - look for specific import error messages

## 📋 **Quick Fix Steps**

### Option A: Use Procfile (Recommended)
```bash
# Delete railway.toml to use Procfile instead
rm railway.toml
git add .
git commit -m "Use Procfile for Railway deployment"
git push
```

### Option B: Use Railway-specific main
```bash
# Keep railway.toml but use main_railway.py
git add .
git commit -m "Add Railway-specific main file"
git push
```

## 🧪 **Testing**
Once deployed, test these endpoints:
- **Root**: `https://your-app.railway.app/` 
- **Health**: `https://your-app.railway.app/health`
- **API Docs**: `https://your-app.railway.app/docs`
- **Balance Check**: `https://your-app.railway.app/accounts/12345/balance`

## 🔍 **Still Having Issues?**

### Debug Information
The `main_railway.py` file includes debug output. Check Railway logs for:
- Import errors
- Current working directory
- Python path information
- Available files

### Environment Variables
Railway automatically provides:
- `PORT` - The port your app should listen on
- `RAILWAY_*` - Various Railway-specific variables

### Last Resort
If nothing works:
1. Delete `railway.toml` 
2. Delete `Procfile`
3. Let Railway auto-detect your Python app
4. Should work with minimal configuration
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
