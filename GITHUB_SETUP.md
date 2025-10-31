# GitHub Repository Setup Instructions

Follow these steps to publish this demo repository to GitHub.

## Prerequisites

- GitHub account
- Git installed locally
- Repository files in `/tmp/mcp-debugpy-demo` (ready to push)

## Step 1: Create GitHub Repository

### Via GitHub Web Interface

1. Go to https://github.com/new
2. Fill in repository details:
   - **Repository name**: `mcp-debugpy-demo`
   - **Description**: `Demo of debugging Python applications with AI using mcp-debugpy`
   - **Visibility**: Public
   - **Initialize**:
     - ❌ Do NOT add README (we have one)
     - ❌ Do NOT add .gitignore (we have one)
     - ❌ Do NOT add license (we have one)
3. Click "Create repository"

### Via GitHub CLI (Alternative)

```bash
cd /tmp/mcp-debugpy-demo
gh repo create mcp-debugpy-demo \
  --public \
  --description "Demo of debugging Python applications with AI using mcp-debugpy" \
  --source=. \
  --push
```

## Step 2: Connect Local Repository to GitHub

If you created the repo via web interface:

```bash
cd /tmp/mcp-debugpy-demo

# Add the remote
git remote add origin https://github.com/markomanninen/mcp-debugpy-demo.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Configure Repository Settings

### Basic Settings

1. Go to repository settings: `https://github.com/markomanninen/mcp-debugpy-demo/settings`
2. Scroll to "Social preview"
3. Click "Edit" and upload a preview image (optional)

### Topics/Tags

Add these topics to help people discover the repo:

```
mcp
debugpy
python
debugging
ai-tools
demo
model-context-protocol
debug-adapter-protocol
ai-assisted-debugging
developer-tools
```

To add via web:
1. Go to main repo page
2. Click gear icon next to "About"
3. Add topics in the "Topics" field

To add via CLI:
```bash
gh repo edit --add-topic "mcp,debugpy,python,debugging,ai-tools,demo,model-context-protocol,debug-adapter-protocol,ai-assisted-debugging,developer-tools"
```

### Repository Details

Update "About" section:
1. Go to main repo page
2. Click gear icon next to "About"
3. Set:
   - **Description**: Demo of debugging Python applications with AI using mcp-debugpy
   - **Website**: https://github.com/markomanninen/mcp-debugpy
   - **Topics**: (as listed above)
   - ✓ Include in the home page

### Enable Features

In Settings → General:
- ✓ Issues
- ✓ Allow forking
- ✓ Sponsorships (optional)
- ✓ Projects (optional)
- ✓ Discussions (optional, good for Q&A)

## Step 4: Add Branch Protection (Optional)

For `main` branch:
1. Go to Settings → Branches
2. Add rule for `main`
3. Configure:
   - ✓ Require pull request reviews before merging
   - ✓ Require status checks to pass before merging

## Step 5: Create Initial Release

### Via Web Interface

1. Go to Releases: `https://github.com/markomanninen/mcp-debugpy-demo/releases`
2. Click "Create a new release"
3. Fill in:
   - **Tag version**: `v1.0.0`
   - **Release title**: `v1.0.0 - Initial Release`
   - **Description**:
     ```markdown
     # MCP Debugpy Demo - Initial Release

     This is the first release of the mcp-debugpy demo repository.

     ## What's Included

     - Shopping cart application with intentional discount bug
     - Comprehensive test suite (10 tests, 3 failing)
     - Complete documentation (README, QUICKSTART, cheat sheet)
     - Automated setup script
     - Pre-configured MCP settings for VS Code and Claude Desktop

     ## Quick Start

     ```bash
     git clone https://github.com/markomanninen/mcp-debugpy-demo.git
     cd mcp-debugpy-demo
     ./setup.sh
     python shopping_cart.py  # See the bug!
     pytest test_shopping_cart.py -v  # See failing tests
     ```

     ## Documentation

     - [README.md](README.md) - Comprehensive guide
     - [QUICKSTART.md](QUICKSTART.md) - Fast-track guide (5 minutes)
     - [CHEATSHEET.md](CHEATSHEET.md) - Quick reference
     - [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md) - Technical details

     ## Requirements

     - Python 3.8+
     - mcp-debugpy (install from GitHub)
     - pytest

     ## The Bug

     The demo includes an intentional bug in the discount calculation:
     - **Expected**: 10% discount on $1,139.96 = $1,025.96
     - **Actual**: $129,950.88 (way off!)

     Use mcp-debugpy with an AI agent to debug and fix it!
     ```
4. Click "Publish release"

### Via CLI

```bash
cd /tmp/mcp-debugpy-demo
gh release create v1.0.0 \
  --title "v1.0.0 - Initial Release" \
  --notes "First release of mcp-debugpy demo with shopping cart bug example"
```

## Step 6: Update Main mcp-debugpy Repository

Add a link to the demo in the main repository's README:

```bash
cd /Users/markomanninen/Downloads/mvp-agent-debug

# Edit README.md to add:
```

Add this section after the "Quick start" section:

```markdown
## Demo Repository

Want to see mcp-debugpy in action? Check out our **[demo repository](https://github.com/markomanninen/mcp-debugpy-demo)**!

The demo includes:
- 🛒 Shopping cart app with an intentional discount bug
- ✅ Test suite that exposes the bug
- 📖 Step-by-step debugging guide
- ⚙️ Pre-configured for VS Code and Claude Desktop

Perfect for learning AI-assisted debugging workflows!
```

## Step 7: Share on Social Media (Optional)

### Twitter/X
```
🚀 New project: mcp-debugpy-demo

Learn AI-assisted debugging with a hands-on demo!

🛒 Shopping cart app with bug
🔍 Debug with AI using MCP
📝 Complete documentation
⚡ Setup in 30 seconds

Try it: https://github.com/markomanninen/mcp-debugpy-demo

#Python #AI #Debugging #MCP
```

### Reddit
Post to r/Python, r/learnprogramming:
```
Title: Demo: Debugging Python Apps with AI Using MCP

I created a demo repository showing how to debug Python applications
using AI agents through the Model Context Protocol (MCP).

The demo includes:
- A shopping cart app with an intentional bug
- AI-powered debugging using natural language
- Complete documentation and setup scripts

Great for learning about AI-assisted debugging!

Repo: https://github.com/markomanninen/mcp-debugpy-demo
```

### Hacker News
```
Title: Demo: AI-Assisted Python Debugging with MCP
URL: https://github.com/markomanninen/mcp-debugpy-demo

A hands-on demo showing how to use AI agents to debug Python code
through the Model Context Protocol (MCP). Includes a shopping cart
app with a subtle bug and guides for debugging it using natural language.
```

## Verification Checklist

After completing the above steps, verify:

- [ ] Repository is public and accessible
- [ ] README displays correctly on GitHub
- [ ] All files are present
- [ ] Topics/tags are visible
- [ ] License is recognized by GitHub
- [ ] Issues are enabled
- [ ] Clone and setup works:
  ```bash
  cd /tmp/test
  git clone https://github.com/markomanninen/mcp-debugpy-demo.git
  cd mcp-debugpy-demo
  ./setup.sh
  python shopping_cart.py
  ```
- [ ] Release is published
- [ ] Link from main mcp-debugpy repo works

## Maintenance

### Updating the Repository

When making changes:

```bash
cd /tmp/mcp-debugpy-demo

# Make changes
# ...

# Commit and push
git add .
git commit -m "Description of changes"
git push origin main

# Tag a new release if significant
git tag -a v1.1.0 -m "Version 1.1.0"
git push origin v1.1.0
gh release create v1.1.0 --generate-notes
```

### Responding to Issues

- Enable GitHub notifications
- Respond to issues within 24-48 hours
- Use labels: `bug`, `enhancement`, `question`, `documentation`
- Close issues with commits: `git commit -m "Fix bug X (closes #123)"`

## Common Issues

### Push Rejected
```bash
# If you see "Updates were rejected"
git pull origin main --rebase
git push origin main
```

### Wrong Remote
```bash
# Update remote URL
git remote set-url origin https://github.com/markomanninen/mcp-debugpy-demo.git
```

### Large Files
```bash
# Remove large files from history if needed
git filter-branch --tree-filter 'rm -f large_file' HEAD
```

## Support

For questions:
- Open an issue: https://github.com/markomanninen/mcp-debugpy-demo/issues
- Discussions: https://github.com/markomanninen/mcp-debugpy-demo/discussions

## License

MIT License - See [LICENSE](LICENSE) file for details.
