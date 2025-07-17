# 🔧 PyCharm Setup Guide for SUDNAXI

## The Problem You're Seeing

When you run `python app.py` directly in PyCharm, you get those "missing ScriptRunContext" errors. This is because Streamlit apps need to be run with the `streamlit run` command, not directly with Python.

## ✅ Quick Fix

Instead of clicking "Run" on `app.py`, do this:

### Option 1: Use the Launcher Script (Recommended)
1. Right-click on `start_app.py` in PyCharm
2. Select "Run 'start_app'"
3. Your app will open in the browser at `http://localhost:8501`

### Option 2: Use the Terminal in PyCharm
1. Open the terminal in PyCharm (View → Tool Windows → Terminal)
2. Run: `streamlit run app.py --server.port=8501`
3. Your app will open in the browser

### Option 3: Configure PyCharm Run Configuration
1. Go to Run → Edit Configurations
2. Click the "+" and add "Python"
3. Set these values:
   - **Name**: SUDNAXI Trading Platform
   - **Script path**: Point to your Python executable
   - **Parameters**: `-m streamlit run app.py --server.port=8501`
   - **Working directory**: Your project folder
4. Click OK and run it

## 🎯 Why This Happens

Streamlit is a web framework that needs to:
- Start a web server
- Handle browser connections
- Manage session state
- Serve the web interface

When you run `python app.py` directly, none of this happens - that's why you get those context errors.

## 🚀 Best Practice for PyCharm

1. **Always use `start_app.py`** - I made this specifically for PyCharm users
2. **Or use the terminal** with `streamlit run app.py`
3. **Never run `app.py` directly** - it won't work

## 📝 PyCharm Configuration Tips

### Set Up a Proper Run Configuration
1. Run → Edit Configurations
2. Add new Python configuration:
   - **Name**: SUDNAXI
   - **Module name**: `streamlit`
   - **Parameters**: `run app.py --server.port=8501`
   - **Working directory**: Your project root

### Terminal Commands That Work
```bash
# Basic startup
streamlit run app.py

# With specific port
streamlit run app.py --server.port=8501

# With custom address
streamlit run app.py --server.address=localhost --server.port=8501
```

## 🔧 If You're Still Having Issues

1. **Check Python Environment**: Make sure you're using the right Python interpreter
2. **Install Dependencies**: Run `pip install -r production_requirements.txt`
3. **Check Working Directory**: Make sure PyCharm is running from the project root
4. **Try the Launcher**: Use `start_app.py` instead of `app.py`

## 💡 Pro Tips

- **Use `start_app.py`** - it handles everything automatically
- **Check the terminal output** - it shows the exact URL to open
- **Use Ctrl+C** to stop the server cleanly
- **The app auto-refreshes** when you change code

## 🎉 You're All Set!

Once you run it correctly with `streamlit run` or `start_app.py`, you'll have a professional trading platform running locally with no errors.

The app will open in your browser and work perfectly - no more context errors!

---

**Happy Trading!** 📈