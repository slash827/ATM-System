# Railway Deployment Guide

## 🚀 **FIXED: Port Variable Expansion Issue**

Railway isn't expanding `$PORT` properly in uvicorn commands. Here are the working solutions:

### **Solution 1: Direct Python Execution (Recommended)**
```
# Procfile
web: python main.py
```
✅ **Uses main.py directly** - handles PORT environment variable internally
✅ **Most reliable** - no shell expansion needed

### **Solution 2: Python Startup Script**
```
# Procfile  
web: python start_server.py
```
✅ **Enhanced error handling** - validates port values
✅ **Debug output** - shows what port is being used

### **Solution 3: Use Gunicorn (Production-Ready)**
```
# Procfile
web: gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```
✅ **Production server** - more robust than uvicorn
✅ **Better for deployment** - handles workers and scaling

## 🔧 **Quick Fix**

**Current Procfile should work:**
```
web: python main.py
```

If not, try the gunicorn approach:
```
web: gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

## 📋 **Why This Happens**

The issue occurs because:
- Railway's shell doesn't expand `$PORT` in uvicorn commands
- Using Python directly bypasses shell expansion
- `main.py` handles `os.environ.get("PORT")` correctly

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
