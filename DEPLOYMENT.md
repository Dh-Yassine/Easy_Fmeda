# FMEDA Web Application - Deployment Guide

This guide will help you deploy the FMEDA web application to production.

## 🏗️ Architecture

- **Frontend**: React.js (deployed on Vercel/Netlify)
- **Backend**: Django REST API (deployed on Heroku/Railway/Render)

## 🚀 Backend Deployment Options

### Option 1: Heroku (Recommended)

1. **Create Heroku Account**
   ```bash
   # Install Heroku CLI
   npm install -g heroku
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   cd fmeda_backend
   heroku create your-fmeda-backend
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY="your-secret-key-here"
   heroku config:set DEBUG="False"
   heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   ```

### Option 2: Railway

1. **Create Railway Account** at railway.app
2. **Connect GitHub Repository**
3. **Set Environment Variables**:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-app-name.railway.app`

### Option 3: Render

1. **Create Render Account** at render.com
2. **Create New Web Service**
3. **Set Environment Variables**
4. **Deploy**

## 🌐 Frontend Deployment Options

### Option 1: Vercel (Recommended)

1. **Create Vercel Account** at vercel.com
2. **Import GitHub Repository**
3. **Set Environment Variables**:
   - `REACT_APP_API_BASE_URL=https://your-backend-domain.herokuapp.com`
4. **Deploy**

### Option 2: Netlify

1. **Create Netlify Account** at netlify.com
2. **Import GitHub Repository**
3. **Set Environment Variables** in Site Settings
4. **Deploy**

## 🔧 Environment Variables

### Backend (Django)
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-app.herokuapp.com
DATABASE_URL=postgresql://...  # If using PostgreSQL
```

### Frontend (React)
```bash
REACT_APP_API_BASE_URL=https://your-backend-domain.herokuapp.com
REACT_APP_ENVIRONMENT=production
```

## 🔄 Update CORS Settings

After deploying your backend, update the CORS settings in `fmeda_backend/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://your-frontend-domain.vercel.app",
    "https://your-frontend-domain.netlify.app",
]
```

## 📁 File Structure for Deployment

```
Fmeda_web/
├── fmeda_backend/          # Django Backend
│   ├── requirements.txt
│   ├── Procfile
│   ├── wsgi.py
│   └── fmeda_backend/
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── fmeda-frontend/         # React Frontend
│   ├── package.json
│   ├── vercel.json
│   ├── netlify.toml
│   └── src/
└── DEPLOYMENT.md
```

## 🚀 Quick Deployment Steps

### 1. Deploy Backend (Heroku)
```bash
cd fmeda_backend
heroku create your-fmeda-backend
heroku config:set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
heroku config:set DEBUG="False"
git push heroku main
heroku run python manage.py migrate
```

### 2. Deploy Frontend (Vercel)
1. Go to vercel.com
2. Import your GitHub repository
3. Set environment variable: `REACT_APP_API_BASE_URL=https://your-fmeda-backend.herokuapp.com`
4. Deploy

### 3. Update CORS
Update the backend CORS settings with your frontend domain.

## 🔍 Testing Deployment

1. **Test Backend**: Visit `https://your-backend.herokuapp.com/projects/`
2. **Test Frontend**: Visit your frontend domain
3. **Test Full Flow**: Create a project, add components, run FMEDA analysis

## 🛠️ Troubleshooting

### Common Issues

1. **CORS Errors**: Check CORS settings in Django
2. **API Connection**: Verify `REACT_APP_API_BASE_URL` is correct
3. **Database Issues**: Run migrations on production
4. **Static Files**: Ensure `STATIC_ROOT` is set correctly

### Debug Commands

```bash
# Check Heroku logs
heroku logs --tail

# Check environment variables
heroku config

# Run Django shell
heroku run python manage.py shell
```

## 🔒 Security Considerations

1. **Secret Key**: Use a strong, unique secret key
2. **Debug Mode**: Always set `DEBUG=False` in production
3. **HTTPS**: Ensure all connections use HTTPS
4. **CORS**: Only allow necessary origins

## 📈 Monitoring

- **Heroku**: Use Heroku's built-in monitoring
- **Vercel**: Use Vercel Analytics
- **Custom**: Add logging to Django views

## 🔄 Continuous Deployment

Set up GitHub Actions or similar CI/CD for automatic deployment on code changes. 