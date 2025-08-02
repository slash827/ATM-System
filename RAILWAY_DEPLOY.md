# Railway Deployment Guide

## � **CRITICAL FIX: Remove railway.toml**

**The issue**: Railway prioritizes `railway.toml` over `Procfile`, and the toml file had the broken `$PORT` syntax.

### **IMMEDIATE FIX (Choose One):**

#### **Option 1: Delete railway.toml (Recommended)**
```bash
# Remove railway.toml to use Procfile only
rm railway.toml
git add .
git commit -m "Remove railway.toml to use Procfile"
git push
```

#### **Option 2: Both Files Fixed (Current State)**
Both `railway.toml` and `Procfile` now use:
```
python main.py
```

### **Why This Happened**
1. Railway prioritizes `railway.toml` over `Procfile`
2. The toml file contained: `uvicorn main:app --port $PORT` 
3. Railway wasn't expanding `$PORT` properly
4. Using `python main.py` bypasses shell expansion

### **Current File Contents**
```
# Procfile
web: python main.py

# railway.toml  
[deploy]
startCommand = "python main.py"
```

## 🎯 **Recommended Action**

**Delete railway.toml completely:**
```bash
rm railway.toml
```

This ensures Railway uses only the Procfile, which is simpler and more reliable.

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
