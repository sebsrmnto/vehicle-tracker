# Install Railway CLI

## Quick Install

**Windows (PowerShell):**
```powershell
iwr https://railway.app/install.ps1 | iex
```

**Or using npm (if you have Node.js):**
```bash
npm i -g @railway/cli
```

**Or using Homebrew (if you have it):**
```bash
brew install railway
```

## After Installation

1. Login:
   ```bash
   railway login
   ```

2. Link to your project:
   ```bash
   railway link
   ```
   - Select your workspace
   - Select "rare-charisma" project
   - Select "production" environment
   - **IMPORTANT:** Select the **MySQL** service (not web)

3. Connect to MySQL:
   ```bash
   railway connect MySQL
   ```

4. Run the SQL command to create users table

