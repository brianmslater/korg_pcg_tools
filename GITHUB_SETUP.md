# GitHub Repository Setup Instructions

Your PCG Tools Python project is now ready for GitHub! Follow these steps to create and push to your repository.

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the **+** icon in the top right → **New repository**
3. Fill in the details:
   - **Repository name**: `pcg-tools-python` (or your preferred name)
   - **Description**: Cross-platform Korg PCG file editor - Python rewrite of PCG Tools
   - **Visibility**: Public (recommended) or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **Create repository**

## Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/pcg-tools-python.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Example:
```bash
git remote add origin https://github.com/johndoe/pcg-tools-python.git
git branch -M main
git push -u origin main
```

## Step 3: Update Repository URLs

After creating the repository, update these files with your actual GitHub username:

### 1. setup.py
Replace `yourusername` in these lines:
```python
url="https://github.com/YOUR_USERNAME/pcg-tools-python",
project_urls={
    "Bug Reports": "https://github.com/YOUR_USERNAME/pcg-tools-python/issues",
    "Source": "https://github.com/YOUR_USERNAME/pcg-tools-python",
    "Documentation": "https://github.com/YOUR_USERNAME/pcg-tools-python#readme",
},
```

### 2. Commit the changes:
```bash
git add setup.py
git commit -m "Update repository URLs"
git push
```

## Step 4: Configure Repository Settings

### Enable Issues
1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll to **Features** section
4. Ensure **Issues** is checked

### Add Topics
1. Go to your repository main page
2. Click the gear icon next to **About**
3. Add topics: `korg`, `synthesizer`, `pcg`, `kronos`, `music`, `audio`, `python`, `cross-platform`
4. Click **Save changes**

### Add Description
In the same **About** section:
- **Description**: Cross-platform Korg PCG file editor - Python rewrite of PCG Tools
- **Website**: (leave blank or add if you have one)

## Step 5: Create First Release

### Tag the Release
```bash
git tag -a v2.0.0 -m "Release v2.0.0 - Complete cross-platform rewrite"
git push origin v2.0.0
```

### Create Release on GitHub
1. Go to your repository
2. Click **Releases** (right sidebar)
3. Click **Create a new release**
4. Choose tag: `v2.0.0`
5. Release title: `v2.0.0 - Production Ready`
6. Description:
   ```markdown
   ## 🎉 PCG Tools Python v2.0.0
   
   Complete cross-platform rewrite of PCG Tools in Python!
   
   ### ✨ Features
   - Full GUI with tkinter (Windows, macOS, Linux)
   - Comprehensive CLI with 7 commands
   - Copy/paste operations
   - Patch editing and organization
   - Report generation
   - Export to CSV/TXT
   - Multiple window support
   
   ### 📦 Installation
   ```bash
   pip install -r requirements.txt
   python -m pcg_tools gui
   ```
   
   ### 📖 Documentation
   - [Quick Start Guide](QUICKSTART.md)
   - [Usage Guide](USAGE.md)
   - [Installation Guide](INSTALL.md)
   
   ### 🙏 Credits
   Inspired by the original PCG Tools by Michel Keijzers
   ```
7. Click **Publish release**

## Step 6: Set Up Branch Protection (Optional)

For collaborative development:

1. Go to **Settings** → **Branches**
2. Click **Add rule**
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
5. Click **Create**

## Step 7: Add Collaborators (Optional)

If working with others:

1. Go to **Settings** → **Collaborators**
2. Click **Add people**
3. Enter GitHub username or email
4. Choose permission level
5. Click **Add**

## What's Already Set Up

Your repository includes:

### ✅ GitHub Actions
- **test.yml**: Runs tests on push/PR (Windows, macOS, Linux)
- **release.yml**: Automates releases when you push tags

### ✅ Issue Templates
- Bug report template
- Feature request template

### ✅ Pull Request Template
- Standardized PR format
- Checklist for contributors

### ✅ Documentation
- README.md (main documentation)
- INSTALL.md (installation guide)
- QUICKSTART.md (5-minute guide)
- USAGE.md (detailed usage)
- CONTRIBUTING.md (developer guide)
- TECHNICAL_REFERENCE.md (format specs)
- CHANGELOG.md (version history)

### ✅ License
- MIT License with acknowledgment to original PCG Tools

### ✅ .gitignore
- Configured for Python projects
- Excludes build artifacts, caches, etc.

## Verification Checklist

After setup, verify:

- [ ] Repository is created on GitHub
- [ ] Local repository is connected (`git remote -v`)
- [ ] Code is pushed (`git push`)
- [ ] README displays correctly on GitHub
- [ ] Issues are enabled
- [ ] Topics are added
- [ ] First release is created
- [ ] GitHub Actions are running (check Actions tab)

## Next Steps

### Promote Your Project
1. Share on Korg Forums
2. Post on Reddit (r/synthesizers, r/korg)
3. Tweet about it
4. Add to awesome-python lists

### Maintain the Project
1. Respond to issues
2. Review pull requests
3. Update documentation
4. Add new features
5. Create new releases

### Monitor
- Watch for GitHub Actions failures
- Check issues regularly
- Review pull requests
- Update dependencies

## Common Commands

```bash
# Check status
git status

# Pull latest changes
git pull

# Create new branch
git checkout -b feature-name

# Commit changes
git add .
git commit -m "Description"
git push

# Create new release
git tag -a v2.1.0 -m "Release v2.1.0"
git push origin v2.1.0

# View remotes
git remote -v

# View branches
git branch -a
```

## Troubleshooting

### Authentication Issues
If you get authentication errors:

**HTTPS (recommended):**
```bash
# Use personal access token
# Create at: Settings → Developer settings → Personal access tokens
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/pcg-tools-python.git
```

**SSH:**
```bash
# Set up SSH key first
git remote set-url origin git@github.com:YOUR_USERNAME/pcg-tools-python.git
```

### Push Rejected
```bash
# Pull first, then push
git pull origin main --rebase
git push
```

### Wrong Remote URL
```bash
# Check current remote
git remote -v

# Update remote URL
git remote set-url origin https://github.com/YOUR_USERNAME/pcg-tools-python.git
```

## Support

- GitHub Issues: For bugs and feature requests
- GitHub Discussions: For questions and community chat
- Pull Requests: For contributions

---

**Your project is ready for the world!** 🚀

Good luck with your open-source project!
