# 🚀 FMEDA Web Application - Complete Deployment Guide

## 📋 Prerequisites
- GitHub account with your repository: `https://github.com/Dh-Yassine/Easy_Fmeda.git`
- Netlify account (free)
- Heroku/Railway/Render account (for backend)

---

## 🔧 Step 1: Deploy Backend (Django) First

### Option A: Deploy to Heroku (Recommended)

1. **Create Heroku Account**
   - Go to [heroku.com](https://heroku.com) and sign up

2. **Install Heroku CLI**
   ```bash
   # Windows (using PowerShell)
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   iwr -useb get.scoop.sh | iex
   scoop install heroku
   ```

3. **Login to Heroku**
   ```bash
   heroku login
   ```

4. **Create Heroku App**
   ```bash
   cd fmeda_backend
   heroku create your-fmeda-backend
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
   heroku config:set DEBUG="False"
   heroku config:set ALLOWED_HOSTS="your-fmeda-backend.herokuapp.com"
   ```

6. **Deploy Backend**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

7. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   ```

8. **Get Your Backend URL**
   - Your backend URL will be: `https://your-fmeda-backend.herokuapp.com`
   - Save this URL for the frontend deployment

### Option B: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub account
3. Create new project from GitHub repo
4. Set root directory to: `fmeda_backend`
5. Add environment variables:
   - `SECRET_KEY`: Generate a random key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-name.railway.app`

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
   - **Value**: `https://your-backend-url.herokuapp.com` (from Step 1)

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
   git push heroku main
   ```

---

## ✅ Step 4: Test Your Deployment

1. **Test Backend**
   - Visit: `https://your-backend-url.herokuapp.com/projects/`
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
# Check Heroku logs
heroku logs --tail

# Check environment variables
heroku config

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
- **Backend**: `https://your-backend-name.herokuapp.com`

Your FMEDA Web Application is now live and ready to use! 🚀

---

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the deployment logs
3. Verify all environment variables are set correctly
4. Ensure both frontend and backend are accessible 