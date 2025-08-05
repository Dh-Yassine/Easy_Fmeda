# 🚀 FMEDA Web Application - Complete Deployment Guide

## 📋 Prerequisites
- GitHub account with your repository: `https://github.com/Dh-Yassine/Easy_Fmeda.git`
- Netlify account (free)
- Railway/Render account (free alternatives to Heroku)

---

## 🔧 Step 1: Deploy Backend (Django) First

### Option A: Deploy to Railway (Recommended - Free Tier)

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app) and sign up with GitHub
   - Railway offers a generous free tier with $5 credit monthly

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository: `Dh-Yassine/Easy_Fmeda`

3. **Configure Backend Deployment**
   - Set **Root Directory** to: `fmeda_backend`
   - Railway will automatically detect it's a Django app

4. **Set Environment Variables**
   - Go to your project → "Variables" tab
   - Add these variables:
     ```
     SECRET_KEY=your-secret-key-here
     DEBUG=False
     ALLOWED_HOSTS=your-app-name.railway.app
     ```

5. **Deploy**
   - Railway will automatically deploy when you push to GitHub
   - Or click "Deploy" to deploy immediately

6. **Get Your Backend URL**
   - Your backend URL will be: `https://your-app-name.railway.app`
   - Save this URL for the frontend deployment

### Option B: Deploy to Render (Free Tier)

1. **Create Render Account**
   - Go to [render.com](https://render.com) and sign up
   - Render offers a free tier with some limitations

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `Dh-Yassine/Easy_Fmeda`

3. **Configure Service**
   - **Name**: `fmeda-backend`
   - **Root Directory**: `fmeda_backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn fmeda_backend.wsgi:application`

4. **Set Environment Variables**
   - Go to "Environment" tab
   - Add variables:
     ```
     SECRET_KEY=your-secret-key-here
     DEBUG=False
     ALLOWED_HOSTS=your-app-name.onrender.com
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically

### Option C: Deploy to Fly.io (Free Tier)

1. **Create Fly.io Account**
   - Go to [fly.io](https://fly.io) and sign up
   - Fly.io offers a generous free tier

2. **Install Fly CLI**
   ```bash
   # Windows (using PowerShell)
   iwr -useb https://fly.io/install.ps1 | iex
   ```

3. **Login and Deploy**
   ```bash
   fly auth login
   cd fmeda_backend
   fly launch
   ```

4. **Set Environment Variables**
   ```bash
   fly secrets set SECRET_KEY="your-secret-key-here"
   fly secrets set DEBUG="False"
   fly secrets set ALLOWED_HOSTS="your-app-name.fly.dev"
   ```

---

## 🌐 Step 2: Deploy Frontend (React) to Netlify

### Method 1: Deploy from GitHub (Recommended)

1. **Go to Netlify**
   - Visit [netlify.com](https://netlify.com)
   - Sign up/Login with your GitHub account

2. **Create New Site**
   - Click "New site from Git"
   - Choose "GitHub"
   - Select your repository: `Dh-Yassine/Easy_Fmeda`

3. **Configure Build Settings**
   - **Base directory**: `fmeda-frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `build`

4. **Set Environment Variables**
   - Click "Show advanced" → "New variable"
   - **Key**: `REACT_APP_API_BASE_URL`
   - **Value**: `https://your-backend-url.railway.app` (from Step 1)

5. **Deploy**
   - Click "Deploy site"
   - Wait for build to complete

6. **Custom Domain (Optional)**
   - Go to "Site settings" → "Domain management"
   - Click "Add custom domain"
   - Enter: `easyfmeda.netlify.app`

### Method 2: Deploy from Local Files

1. **Build the Frontend Locally**
   ```bash
   cd fmeda-frontend
   npm install
   npm run build
   ```

2. **Deploy to Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Drag and drop the `build` folder
   - Set environment variable: `REACT_APP_API_BASE_URL`

---

## 🔗 Step 3: Update CORS Settings (If Needed)

If you get CORS errors, update the backend CORS settings:

1. **Go to your backend deployment**
2. **Update CORS settings** in `fmeda_backend/settings.py`:
   ```python
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "https://easyfmeda.netlify.app",
       "https://easyfmeda.vercel.app",
   ]
   ```

3. **Redeploy backend**:
   ```bash
   git add .
   git commit -m "Update CORS settings"
   git push origin master
   ```

---

## ✅ Step 4: Test Your Deployment

1. **Test Backend**
   - Visit: `https://your-backend-url.railway.app/projects/`
   - Should show Django REST API interface

2. **Test Frontend**
   - Visit: `https://easyfmeda.netlify.app`
   - Should load the FMEDA application

3. **Test Full Flow**
   - Create a new project
   - Add safety functions
   - Add components
   - Add failure modes
   - Run FMEDA analysis

---

## 🛠️ Troubleshooting

### Common Issues:

1. **"Page not found" Error**
   - Make sure you set the correct **Base directory** to `fmeda-frontend`
   - Check that **Publish directory** is set to `build`

2. **CORS Errors**
   - Update CORS settings in backend
   - Make sure frontend URL is in `CORS_ALLOWED_ORIGINS`

3. **Build Failures**
   - Check that all dependencies are in `package.json`
   - Verify Node.js version compatibility

4. **API Connection Issues**
   - Verify `REACT_APP_API_BASE_URL` is correct
   - Check that backend is running and accessible

### Debug Commands:

```bash
# Check Railway logs
railway logs

# Check Render logs
# Go to your service dashboard → "Logs" tab

# Check Fly.io logs
fly logs

# Test backend locally
cd fmeda_backend
python manage.py runserver

# Test frontend locally
cd fmeda-frontend
npm start
```

---

## 🎯 Final URLs

After successful deployment:

- **Frontend**: `https://easyfmeda.netlify.app`
- **Backend**: `https://your-backend-name.railway.app` (or .onrender.com, .fly.dev)

Your FMEDA Web Application is now live and ready to use! 🚀

---

## 💰 Free Tier Comparison

| Platform | Free Tier | Pros | Cons |
|----------|-----------|------|------|
| **Railway** | $5/month credit | Easy setup, auto-deploy | Limited to $5 credit |
| **Render** | Free web services | Simple deployment | Sleeps after 15min inactivity |
| **Fly.io** | 3 shared VMs free | Fast, global | More complex setup |
| **Netlify** | Free hosting | Great for frontend | Backend not supported |

---

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the deployment logs
3. Verify all environment variables are set correctly
4. Ensure both frontend and backend are accessible 