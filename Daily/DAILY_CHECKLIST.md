# ✅ Daily Workflow Checklist

**Use this every time you work on your project!**

---

## 🏁 STARTING WORK

- [ ] Open project folder
- [ ] Pull latest changes: `git pull` (if using Git)
- [ ] Ready to code!

---

## 💻 WHILE WORKING

- [ ] **Save files frequently** (`Ctrl+S`)
- [ ] Test changes: `python app.py`
- [ ] Verify changes work in browser
- [ ] Stop server when done testing: `Ctrl+C`

---

## 🏁 FINISHING WORK (Before You Leave!)

### Step 1: Save Everything
- [ ] Save all files (`Ctrl+K S` or save each file)
- [ ] Close any temporary/test files

### Step 2: Test Locally
- [ ] Run app: `python app.py`
- [ ] Test main features work
- [ ] No errors in terminal
- [ ] Stop server: `Ctrl+C`

### Step 3: Commit to Git
- [ ] Check status: `git status`
- [ ] Add changes: `git add .`
- [ ] Commit: `git commit -m "What you did"`
- [ ] Push: `git push`

### Step 4: Deploy to Railway
- [ ] Wait 1-2 minutes after `git push`
- [ ] Check Railway dashboard → Deployments
- [ ] Verify deployment succeeded (green checkmark)
- [ ] Test live site (visit your Railway URL)
- [ ] Everything works? ✅ Done!

---

## 🚨 QUICK COMMANDS

```bash
# Save & Test
python app.py                    # Run app
# Then visit: http://localhost:5000
# Press Ctrl+C to stop

# Save to Git
git status                       # See what changed
git add .                        # Add all changes
git commit -m "Your message"     # Save with message
git push                         # Upload to GitHub

# Railway auto-deploys when you push!
```

---

## 📝 COMMIT MESSAGE EXAMPLES

✅ **Good:**
- `"Add input validation to forms"`
- `"Fix favicon display issue"`
- `"Update README with new features"`
- `"Add CSV export functionality"`

❌ **Bad:**
- `"changes"`
- `"update"`
- `"fix"`
- `"stuff"`

---

## ⚡ EMERGENCY: Quick Save

**If you need to save quickly and leave:**

```bash
git add .
git commit -m "WIP: Work in progress"
git push
```

Then continue later!

---

**Print this and keep it next to your computer!** 📌

