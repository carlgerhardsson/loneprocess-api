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

## ⚠️ IMPORTANT: Rate Limiting

**API är begränsat till 60 requests per minut per IP-adress**

### Quick Facts:
- ✅ Max 60 requests/minute
- ✅ Average: 1 request/second
- ❌ HTTP 429 if exceeded
- 🔄 Retry after 60 seconds

### Response Headers:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1678901234
```

### Best Practice:
```javascript
// Always check rate limit headers
const response = await fetch(url, options);
const remaining = response.headers.get('X-RateLimit-Remaining');

if (remaining < 10) {
  console.warn('⚠️ Approaching rate limit!');
}
```

**📖 Full details:** [RATE_LIMITING.md](RATE_LIMITING.md)

---

## 📚 Documentation

### **Quick References:**
- [Integration Guide](INTEGRATION_GUIDE.md) - Step-by-step integration
- [Firebase Setup](FIREBASE_SETUP.md) - Authentication setup
- [Test Data](TEST_DATA.md) - Available test data
- [Rate Limiting](RATE_LIMITING.md) - **IMPORTANT** Cost control
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

## 🔒 Security

- ✅ **Read-only access** - You cannot modify data
- ✅ **Test data only** - No production or sensitive data
- ✅ **Token-based auth** - Firebase Authentication required
- ✅ **Rate limited** - 60 requests/minute (cost control)
- ✅ **HTTPS enforced** - All traffic encrypted

### Important:
- Never commit tokens to Git
- Store tokens in environment variables
- Don't share tokens between teams
- Report security issues immediately
- **Respect rate limits** - They protect against unexpected costs

---

## 📊 Available Test Data

- **100 employees** - Swedish names, realistic org codes
- **12 salary periods** - Jan-Dec 2025
- **50 activities** - All process phases
- **120 errors** - Various severities
- **240 assignments** - Activities linked to periods

See [TEST_DATA.md](TEST_DATA.md) for details.

---

## 💬 Support

**Need help?**

- **Email:** carl.gerhardsson@cgi.com
- **Response time:** Within 24 hours
- **GitHub Issues:** [Report here](https://github.com/carlgerhardsson/loneprocess-api/issues)

**Rate limit too low?**
Contact us to discuss your use case. We can adjust limits if needed.

---

## 🔄 API Status

**Current Version:** 3.0.0-staging

**Status:** ✅ Active

**Rate Limit:** 60 req/min

**Last Updated:** 2026-03-11

---

**Happy coding! 🚀**
