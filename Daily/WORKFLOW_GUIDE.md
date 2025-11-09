# 📝 Workflow Guide - Saving & Deploying Your Work

A step-by-step guide to save your work locally and deploy to Railway (production).

---

## 🎯 Quick Reference

### Before You Start Working
1. ✅ Pull latest changes (if using Git)
2. ✅ Check current branch
3. ✅ Test that app runs locally

### While Working
1. ✅ Save files frequently (`Ctrl+S`)
2. ✅ Test changes locally
3. ✅ Commit changes regularly

### Before Leaving Work
1. ✅ Save all files
2. ✅ Test everything works
3. ✅ Commit changes to Git
4. ✅ Push to GitHub
5. ✅ Verify Railway auto-deploys

---

## 📂 Part 1: Local Development (Saving Your Work)

### Step 1: Save Your Files
**Always save before testing or deploying!**

- **Single file**: `Ctrl+S` (Windows) or `Cmd+S` (Mac)
- **Save all files**: `Ctrl+K S` (VS Code) or `Ctrl+Shift+S`
- **Auto-save**: Enable in your editor settings

### Step 2: Test Locally
```bash
# Make sure you're in your project folder
cd "C:\Users\sebas\OneDrive\Desktop\vehicle tracker"

# Run the app
python app.py
```

**Check:**
- ✅ App starts without errors
- ✅ Pages load correctly
- ✅ Forms work
- ✅ No console errors (F12 → Console tab)

### Step 3: Stop the Server
- Press `Ctrl+C` in the terminal to stop the server

---

## 🔄 Part 2: Git Workflow (Version Control)

### Initial Setup (One-time only)
If you haven't set up Git yet:

```bash
# Initialize Git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit"

# Connect to GitHub (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/vehicle-tracker.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Daily Workflow (Every Time You Work)

#### 1. Check Status
```bash
git status
```
This shows what files you've changed.

#### 2. Add Changes
```bash
# Add all changed files
git add .

# OR add specific files
git add app.py templates/index.html
```

#### 3. Commit Changes
```bash
git commit -m "Description of what you changed"
```

**Good commit messages:**
- ✅ `"Add input validation to vehicle forms"`
- ✅ `"Fix favicon caching issue"`
- ✅ `"Update README with new features"`
- ❌ `"changes"` (too vague)
- ❌ `"fix"` (not descriptive)

#### 4. Push to GitHub
```bash
git push
```

**If it's your first push:**
```bash
git push -u origin main
```

---

## 🚀 Part 3: Deploying to Railway (Production)

### Automatic Deployment (Recommended)

Railway automatically deploys when you push to GitHub!

**Steps:**
1. ✅ Make your changes locally
2. ✅ Test everything works
3. ✅ Commit changes: `git commit -m "Your message"`
4. ✅ Push to GitHub: `git push`
5. ✅ Railway automatically detects the push
6. ✅ Wait 1-2 minutes for deployment
7. ✅ Check Railway dashboard → Deployments tab
8. ✅ Visit your live site to verify

### Manual Deployment (If Needed)

If auto-deploy isn't working:

1. Go to Railway Dashboard
2. Select your project
3. Go to **Deployments** tab
4. Click **"Redeploy"** on latest deployment

---

## ✅ Pre-Leave Checklist (Before You Stop Working)

Use this checklist every time before you finish working:

### Local Work
- [ ] **Save all files** (`Ctrl+S` or `Ctrl+K S`)
- [ ] **Test app runs** (`python app.py` - should start without errors)
- [ ] **Stop the server** (`Ctrl+C`)

### Git & Version Control
- [ ] **Check what changed**: `git status`
- [ ] **Add changes**: `git add .`
- [ ] **Commit changes**: `git commit -m "Description"`
- [ ] **Push to GitHub**: `git push`

### Deployment
- [ ] **Check Railway dashboard** - verify latest deployment succeeded
- [ ] **Test live site** - visit your Railway URL, make sure it works
- [ ] **Check logs** (if needed) - Railway → Deployments → View logs

### Clean Up
- [ ] **Close unnecessary files** in your editor
- [ ] **Close terminal** (optional)
- [ ] **Note what you worked on** (for next session)

---

## 🔧 Common Commands Cheat Sheet

### Git Commands
```bash
# Check what files changed
git status

# See what changed in a file
git diff app.py

# Add all changes
git add .

# Commit changes
git commit -m "Your message here"

# Push to GitHub
git push

# Pull latest changes (if working on multiple computers)
git pull

# View commit history
git log --oneline
```

### Local Development
```bash
# Run the app
python app.py

# Install new packages
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### Railway CLI (Optional)
```bash
# Login to Railway
railway login

# Link to project
railway link

# View logs
railway logs

# Open in browser
railway open
```

---

## 🐛 Troubleshooting

### "Nothing to commit"
**Problem**: `git status` shows "nothing to commit"

**Solution**: 
- You haven't made any changes, OR
- You haven't saved your files yet (`Ctrl+S`)

### "Changes not showing on live site"
**Problem**: Pushed to GitHub but Railway site hasn't updated

**Solutions**:
1. Wait 1-2 minutes (deployment takes time)
2. Check Railway dashboard → Deployments tab
3. Look for errors in deployment logs
4. Try manual redeploy

### "Can't push to GitHub"
**Problem**: `git push` fails

**Solutions**:
1. Make sure you're logged into GitHub
2. Check you have write access to the repository
3. Try: `git pull` first, then `git push`
4. If still fails, check your Git credentials

### "App won't start locally"
**Problem**: `python app.py` gives errors

**Solutions**:
1. Check you're in the right folder
2. Make sure all dependencies installed: `pip install -r requirements.txt`
3. Check for syntax errors in your code
4. Look at the error message - it usually tells you what's wrong

---

## 📋 Daily Workflow Example

### Morning (Starting Work)
```bash
# 1. Open project folder
cd "C:\Users\sebas\OneDrive\Desktop\vehicle tracker"

# 2. Pull latest changes (if using Git with others)
git pull

# 3. Start working
# ... make your changes ...

# 4. Save files frequently
# Ctrl+S, Ctrl+S, Ctrl+S...
```

### During Work
```bash
# Test changes
python app.py
# Open browser: http://localhost:5000
# Test your changes
# Stop server: Ctrl+C
```

### End of Day (Finishing Work)
```bash
# 1. Save all files
# Ctrl+K S (or save each file)

# 2. Test one last time
python app.py
# Verify everything works
# Ctrl+C to stop

# 3. Commit and push
git status                    # See what changed
git add .                     # Add all changes
git commit -m "Add new feature X"  # Commit
git push                      # Push to GitHub

# 4. Check Railway
# Go to Railway dashboard
# Verify deployment succeeded
# Test live site
```

---

## 🎓 Best Practices

### 1. Commit Often
- ✅ Commit after completing a feature
- ✅ Commit after fixing a bug
- ✅ Don't wait until end of day

### 2. Write Good Commit Messages
- ✅ Be descriptive: "Add CSV export feature"
- ✅ Use present tense: "Fix validation bug"
- ❌ Avoid: "update", "changes", "fix"

### 3. Test Before Pushing
- ✅ Always test locally first
- ✅ Make sure app starts without errors
- ✅ Test the feature you just added

### 4. Keep It Clean
- ✅ Don't commit temporary files
- ✅ Don't commit `.env` files (with passwords)
- ✅ Use `.gitignore` for files that shouldn't be tracked

### 5. Regular Backups
- ✅ Push to GitHub regularly (it's your backup!)
- ✅ Railway keeps deployment history
- ✅ Git keeps all your commit history

---

## 📱 Quick Reference Card

**Print this and keep it handy!**

```
┌─────────────────────────────────────┐
│  DAILY WORKFLOW                     │
├─────────────────────────────────────┤
│  1. Save: Ctrl+S                    │
│  2. Test: python app.py             │
│  3. Commit: git add .               │
│     git commit -m "message"         │
│  4. Push: git push                  │
│  5. Check Railway dashboard         │
└─────────────────────────────────────┘
```

---

## 🆘 Need Help?

1. **Git issues**: Check `git status` and error messages
2. **Railway issues**: Check Railway dashboard → Logs
3. **Local issues**: Check terminal error messages
4. **Code issues**: Use your editor's error highlighting

---

## 📝 Notes Section

Use this space to note what you're working on:

**Today's Work:**
- [ ] 
- [ ] 
- [ ] 

**Next Session:**
- [ ] 
- [ ] 
- [ ] 

---

**Remember**: Save early, save often, commit regularly, and always test before pushing! 🚀

