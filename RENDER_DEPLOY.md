# Render Deployment Guide: Faculty Finder (100% Free)

## ✅ Prerequisites Fixed
The following issues have been resolved for successful deployment:
- ❌ **FIXED**: Removed `sqlite3` from `requirements.txt` (it's a built-in Python module)
- ❌ **FIXED**: Changed host binding from `127.0.0.1` to `0.0.0.0` in `run.py`
- ❌ **FIXED**: Added PORT environment variable support for Render
- ❌ **FIXED**: Disabled reload mode for production deployment

## 🚀 Deployment Steps

### Step 1: Push to GitHub
If you haven't already, create a repository and push your code:
```bash
git add .
git commit -m "Fixed Render deployment configuration"
git push origin main
```

### Step 2: Create Web Service on Render
1. Go to [Render.com](https://render.com) and sign in
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `faculty-finder` (or your preferred name)
   - **Runtime**: **Docker**
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Instance Type**: **Free**

### Step 3: Deploy
- Click **Create Web Service**
- Render will automatically:
  - Build your Docker image using the `Dockerfile`
  - Install dependencies from `requirements.txt`
  - Start your application on the assigned PORT
  - Provide a public URL (e.g., `https://faculty-finder-xxxx.onrender.com`)

### Step 4: Verify Deployment
After deployment completes (usually 2-5 minutes):
1. Visit your Render URL
2. You should see: `{"message": "Faculty Finder AI Engine is Running", ...}`
3. Access the dashboard at: `https://your-app.onrender.com/static/index.html`
4. API docs available at: `https://your-app.onrender.com/docs`

## 📝 Important Notes

### Free Tier Limitations
- **Spin Down**: Service sleeps after 15 minutes of inactivity
- **Spin Up**: First request after sleep takes ~30-60 seconds
- **Build Time**: Limited to 15 minutes (your app builds in ~2-3 minutes)
- **Bandwidth**: 100 GB/month

### Database Persistence
- The SQLite database (`faculty.db`) is included in your Docker image
- **Note**: Any runtime changes to the database will be lost on redeploy
- For persistent data, consider upgrading to a PostgreSQL database on Render

### Troubleshooting
If deployment fails:
1. Check Render logs for specific errors
2. Verify all files are committed to Git
3. Ensure `faculty.db` exists in your repository
4. Check that `app/static/` directory exists with UI files

## 🎉 Success!
Your Faculty Finder AI Engine is now live and accessible worldwide!
