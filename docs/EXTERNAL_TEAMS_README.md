# Löneprocess API - External Team Documentation

**Welcome to the Löneprocess API!**

This documentation is for external teams integrating with our staging API.

---

## 🚀 Quick Start

### 1. Get Access

Contact your API administrator:
- **Email:** carl.gerhardsson@cgi.com
- **Response time:** Within 24 hours

You will receive:
- Firebase custom token
- Firebase API key
- Access instructions

### 2. Authentication Setup

```javascript
import { initializeApp } from 'firebase/app';
import { getAuth, signInWithCustomToken } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "loneprocess-api-staging.firebaseapp.com",
  projectId: "loneprocess-api-staging"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Authenticate with your custom token
const customToken = 'YOUR_CUSTOM_TOKEN';
const userCredential = await signInWithCustomToken(auth, customToken);
const idToken = await userCredential.user.getIdToken();
```

### 3. Make API Calls

```javascript
const response = await fetch('http://localhost:8000/api/v1/loneperiods', {
  headers: {
    'Authorization': `Bearer ${idToken}`,
    'Content-Type': 'application/json'
  }
});

const periods = await response.json();
```

---

## 📚 Documentation

### **Quick References:**
- [Integration Guide](INTEGRATION_GUIDE.md) - Step-by-step integration
- [Firebase Setup](FIREBASE_SETUP.md) - Authentication setup
- [Test Data](TEST_DATA.md) - Available test data
- [Code Examples](examples/) - JS, TS, cURL examples

---

## 🌐 API Endpoints

**Base URL:** `http://localhost:8000` (staging)

**Swagger Documentation:** http://localhost:8000/docs

### Main Endpoints:

```
GET  /api/v1/loneperiods           # List salary periods
GET  /api/v1/loneperiods/{id}      # Get specific period
GET  /api/v1/activities            # List activities
GET  /api/v1/la/employees          # List employees
GET  /api/v1/la/fellistor/{id}     # Get error list
```

---

## 📋 Available Test Data

- **100 employees** - Swedish names, realistic org codes
- **12 salary periods** - Jan-Dec 2025
- **50 activities** - All process phases
- **120 errors** - Various severities
- **240 assignments** - Activities linked to periods

See [TEST_DATA.md](TEST_DATA.md) for details.

---

## 🔒 Security

- ✅ **Read-only access** - You cannot modify data
- ✅ **Test data only** - No production or sensitive data
- ✅ **Token-based auth** - Firebase Authentication required
- ✅ **Rate limited** - 100 requests/minute
- ✅ **HTTPS enforced** - All traffic encrypted

### Important:
- Never commit tokens to Git
- Store tokens in environment variables
- Don't share tokens between teams
- Report security issues immediately

---

## 💬 Support

**Need help?**

- **Email:** carl.gerhardsson@cgi.com
- **Response time:** Within 24 hours
- **GitHub Issues:** [Report here](https://github.com/carlgerhardsson/loneprocess-api/issues)

---

## 🔄 API Status

**Current Version:** 3.0.0-staging

**Status:** ✅ Active

**Last Updated:** 2026-03-10

---

**Happy coding! 🚀**
