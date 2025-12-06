# TROUBLESHOOTING GUIDE for Bella Bot

## Issue: ModuleNotFoundError: No module named 'bot'

This happens when Python cannot find the `bot` package. The issue is likely one of:

1. **Missing __init__.py files** — Python packages need `__init__.py` in each directory
2. **pip install not completed** — `pip install -e .` didn't finish properly
3. **Wrong Python interpreter** — running a different Python than the one with installed packages
4. **PATH issues** — pip-installed scripts (like uvicorn) not in PATH

## Diagnostic Steps

### Step 1: Run the Diagnostic Script
```powershell
# From repo root
.\scripts\diagnose.ps1
```

This will check:
- ✅ Python version and location
- ✅ pip version and site-packages path
- ✅ If bella-bot package is installed
- ✅ If __init__.py files exist
- ✅ If all dependencies are installed
- ✅ If uvicorn is available
- ✅ If bot.bella_bot can be imported

### Step 2: Manual Fix (if diagnostic shows issues)

```powershell
# Navigate to bot directory
cd D:\pRoG\bella-bot-v2\bot

# Ensure __init__.py files exist
# (diagnostic script should create them if missing)

# Upgrade pip
python -m pip install --upgrade pip

# Install the bot package in editable mode
python -m pip install -e .

# Verify uvicorn installed
python -m pip install uvicorn

# Test the import
python -c "import bot.bella_bot; print('✅ Import successful')"

# Test uvicorn is available
uvicorn --version

# If uvicorn still not found, run directly via python
python -m uvicorn bot.bella_bot.api_server:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: If Still Failing

Check Python path:
```powershell
# See which Python is being used
Get-Command python

# See installed packages
python -m pip list

# See site-packages location
python -c "import site; print(site.getsitepackages())"

# See where bot.bella_bot should be installed
python -c "import bot.bella_bot; import os; print(os.path.dirname(bot.bella_bot.__file__))"
```

## Common Issues & Fixes

### Issue: "No module named 'bot'"
**Cause:** pip install didn't complete or __init__.py missing  
**Fix:**
```powershell
cd bot
python -m pip install -e .
```

### Issue: "uvicorn is not recognized"
**Cause:** uvicorn not installed or Scripts folder not in PATH  
**Fix:**
```powershell
# Install uvicorn
python -m pip install uvicorn

# Or use python -m to run it
python -m uvicorn bot.bella_bot.api_server:app --reload
```

### Issue: "Discord client ID is not configured"
**Cause:** .env file missing required variables  
**Fix:**
```powershell
# Check .env exists
Get-Content .env

# Should have VITE_DISCORD_CLIENT_ID, VITE_DISCORD_REDIRECT_URI, etc.
# Edit .env and add your Discord OAuth credentials
```

### Issue: "Authentication Error"
**Cause:** Discord OAuth settings misconfigured  
**Fix:**
1. Go to Discord Developer Portal: https://discord.com/developers/applications
2. Create or select your bot application
3. Go to OAuth2 > General
4. Copy the **Client ID** to `VITE_DISCORD_CLIENT_ID` in .env
5. Go to OAuth2 > General and copy **Client Secret** to `VITE_DISCORD_CLIENT_SECRET`
6. Add Redirect URL: `http://localhost:5173/auth/discord/callback`
7. Copy that URL to `VITE_DISCORD_REDIRECT_URI` in .env

## Recommended: Full Clean Install

If issues persist, start fresh:

```powershell
# From repo root
cd bot

# Remove old installation artifacts
pip uninstall bella-bot -y
rm -r bella_bot.egg-info
rm -r __pycache__

# Reinstall
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .

# Verify
python -c "import bot.bella_bot; print('✅ Ready to go!')"
```

Then run:
```powershell
cd ..
.\scripts\setup_and_run.ps1
```

---

**Still stuck?** Open an issue or check the logs in the console windows.
