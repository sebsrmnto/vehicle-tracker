# ⚡ Quick GitHub Setup (5 Minutes)

## ⚠️ SECURITY WARNING FIRST!

Your `db_config.py` contains a password. **Before pushing to GitHub:**

### Quick Fix Options:

**Option A: Remove password temporarily**
- Open `db_config.py`
- Change password to `"YOUR_PASSWORD_HERE"` or empty string
- Commit this version
- Keep your real password locally

**Option B: Use environment variables** (Better for future)
- See `GITHUB_SETUP.md` for detailed instructions
- Use `db_config.example.py` as a template

---

## 🚀 Quick Steps

### 1. Make Your First Commit
```bash
git commit -m "Initial commit: Vehicle Tracker app with maintenance log feature"
```

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `vehicle-tracker`
3. Description: "Vehicle maintenance tracker - Flask & MySQL"
4. Choose **Public** or **Private**
5. **DON'T** check "Initialize with README" (you already have one)
6. Click **"Create repository"**

### 3. Connect and Push

**Copy these commands** (replace YOUR_USERNAME):

```bash
git remote add origin https://github.com/YOUR_USERNAME/vehicle-tracker.git
git branch -M main
git push -u origin main
```

**If you get an error about "main" vs "master":**
```bash
git branch -M main
git push -u origin main
```

**Or if your default is "master":**
```bash
git push -u origin master
```

---

## ✅ Done!

Your code is now on GitHub! Visit: `https://github.com/YOUR_USERNAME/vehicle-tracker`

---

## 📋 What's Included

- ✅ All your code files
- ✅ Documentation (GUIDE.md, NOTES.md)
- ✅ README.md
- ✅ .gitignore (protects sensitive files)
- ⚠️ db_config.py (contains password - consider removing it first!)

---

## 🔍 Check Before Pushing

```bash
git status  # See what will be committed
```

Make sure no sensitive files are included!

---

**Need more details? See `GITHUB_SETUP.md`**

