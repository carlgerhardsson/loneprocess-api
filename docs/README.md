# Documentation Overview

**All project documentation for Löneprocess Digital Checklista API**

---

## 📚 Documentation Structure

### **For Internal Team:**
- [PROJECT_HISTORY.md](PROJECT_HISTORY.md) - **START HERE!** Complete project timeline
- [LESSONS_LEARNED.md](LESSONS_LEARNED.md) - Best practices and pitfalls
- [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) - **NEW!** How to develop new endpoints
- [CLAUDE_VSCODE_GITHUB_WORKFLOW.md](CLAUDE_VSCODE_GITHUB_WORKFLOW.md) - Development workflow

### **For External Teams:**
- [EXTERNAL_TEAMS_README.md](EXTERNAL_TEAMS_README.md) - **START HERE!** Quick start guide
- [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - Step-by-step integration
- [FIREBASE_SETUP.md](FIREBASE_SETUP.md) - Authentication setup
- [TEST_DATA.md](TEST_DATA.md) - Available test data

### **Code Examples:**
- [examples/](examples/) - JavaScript, TypeScript, cURL examples

---

## 🚀 Quick Links

**For Developers:**
- Local API: http://localhost:8000/docs
- GitHub Repo: https://github.com/carlgerhardsson/loneprocess-api
- Firebase Console: https://console.firebase.google.com/project/loneprocess-api-staging
- Public Docs: https://github.com/carlgerhardsson/loneprocess-api-docs

**For External Teams:**
- Public Docs: https://github.com/carlgerhardsson/loneprocess-api-docs
- Request access: carl.gerhardsson@cgi.com

---

## 📖 What to Read When

### **New to the project?**
1. Read [PROJECT_HISTORY.md](PROJECT_HISTORY.md) - Get full context
2. Read [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) - Understand how we work

### **Adding a new feature?**
1. Read [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) - Follow the process
2. Check [LESSONS_LEARNED.md](LESSONS_LEARNED.md) - Avoid common mistakes

### **Troubleshooting?**
1. Check [LESSONS_LEARNED.md](LESSONS_LEARNED.md) - Common issues & solutions
2. Check Firebase Console logs

### **Integrating as external team?**
1. Go to https://github.com/carlgerhardsson/loneprocess-api-docs
2. Start with README → Integration Guide → Examples

---

## 📊 Repository Structure

```
loneprocess-api/ (PRIVATE)
├── main branch (SQLite backend + docs)
└── staging branch (Firebase backend + docs)

loneprocess-api-docs/ (PUBLIC)
└── main branch (External documentation only)
```

**All internal documentation is in this /docs folder.**

---

**Last Updated:** 2026-03-11  
**Maintainer:** Carl Gerhardsson
