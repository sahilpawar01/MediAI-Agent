# Deployment Guide

## Best Option: Hugging Face Spaces (Recommended) ⭐

**Why Hugging Face Spaces?**
- ✅ Free tier with generous limits
- ✅ Built specifically for Gradio apps
- ✅ Easy deployment (just push to Git)
- ✅ Automatic HTTPS
- ✅ Built-in environment variable management
- ✅ No credit card required

### Steps to Deploy on Hugging Face Spaces:

1. **Create a Hugging Face account** (if you don't have one)
   - Go to https://huggingface.co/join

2. **Create a new Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Name: `med-ai-doctor` (or your preferred name)
   - SDK: Select **"Gradio"**
   - Hardware: CPU Basic (free) is fine
   - Visibility: Public or Private

3. **Push your code**
   - Clone the Space repository:
     ```bash
     git clone https://huggingface.co/spaces/YOUR_USERNAME/med-ai-doctor
     ```
   - Copy your files to the repository:
     - `app.py` (use this instead of gradio_app.py)
     - `brain_of_the_doctor.py`
     - `voice_of_the_patient.py`
     - `voice_of_the_doctor.py`
     - `requirements_clean.txt` (rename to `requirements.txt`)
   - Commit and push:
     ```bash
     git add .
     git commit -m "Initial deployment"
     git push
     ```

4. **Add API Keys as Secrets**
   - Go to your Space settings
   - Click "Variables and secrets"
   - Add two secrets:
     - `GROQ_API_KEY` = your Groq API key
     - `GEMINI_API_KEY` = your Gemini API key
   - Save

5. **Wait for build** (usually 2-5 minutes)
   - Your app will be live at: `https://YOUR_USERNAME-med-ai-doctor.hf.space`

---

## Option 2: Render

**Why Render?**
- ✅ Free tier available
- ✅ Easy deployment from GitHub
- ✅ Automatic HTTPS
- ✅ Good for Python apps

### Steps to Deploy on Render:

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Create a Render account**
   - Go to https://render.com
   - Sign up with GitHub

3. **Create a new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `med-ai-doctor`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements_clean.txt`
     - **Start Command**: `python app.py`
     - **Plan**: Free (or paid for better performance)

4. **Add Environment Variables**
   - In the Render dashboard, go to your service
   - Click "Environment"
   - Add:
     - `GROQ_API_KEY` = your Groq API key
     - `GEMINI_API_KEY` = your Gemini API key

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (usually 5-10 minutes)
   - Your app will be live at: `https://med-ai-doctor.onrender.com`

---

## Option 3: Railway

Similar to Render, Railway is also a good option:
- Go to https://railway.app
- Connect GitHub
- Deploy with similar settings

---

## Important Notes:

1. **Use `app.py` for deployment** (not `gradio_app.py`)
   - `app.py` is optimized for production

2. **Use `requirements_clean.txt`** (rename to `requirements.txt` for deployment)
   - This version doesn't have the `-i` flag

3. **Never commit `.env` file**
   - It's already in `.gitignore`
   - Always use environment variables/secrets in the platform

4. **Free tier limitations:**
   - Apps may sleep after inactivity (Render)
   - Some platforms have usage limits
   - Hugging Face Spaces is usually the most reliable for free tier

---

## Quick Comparison:

| Platform | Free Tier | Best For | Setup Difficulty |
|----------|-----------|----------|------------------|
| **Hugging Face Spaces** | ✅ Yes | Gradio apps | ⭐ Easy |
| **Render** | ✅ Yes | General apps | ⭐⭐ Medium |
| **Railway** | ✅ Yes (limited) | General apps | ⭐⭐ Medium |

**Recommendation: Start with Hugging Face Spaces!**

