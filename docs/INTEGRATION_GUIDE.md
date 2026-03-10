# Integration Guide

Complete guide for integrating with the Löneprocess API.

---

## 📋 Prerequisites

1. **Firebase custom token** from API administrator
2. **Firebase SDK** installed in your project
3. **HTTPS client** (fetch, axios, etc.)

---

## 🔥 Step-by-Step Integration

### Step 1: Install Firebase SDK

```bash
npm install firebase
```

### Step 2: Initialize Firebase

```javascript
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "Get from admin",
  authDomain: "loneprocess-api-staging.firebaseapp.com",
  projectId: "loneprocess-api-staging"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
```

### Step 3: Authenticate

```javascript
import { signInWithCustomToken } from 'firebase/auth';

const customToken = process.env.FIREBASE_CUSTOM_TOKEN;

try {
  const userCredential = await signInWithCustomToken(auth, customToken);
  console.log('✅ Authenticated!');
} catch (error) {
  console.error('❌ Auth failed:', error.message);
}
```

### Step 4: Get ID Token

```javascript
const user = auth.currentUser;
const idToken = await user.getIdToken();
```

### Step 5: Make API Requests

```javascript
const response = await fetch('http://localhost:8000/api/v1/loneperiods', {
  headers: {
    'Authorization': `Bearer ${idToken}`,
    'Content-Type': 'application/json'
  }
});

const periods = await response.json();
console.log(`Found ${periods.length} periods`);
```

---

## 🔄 Token Refresh

ID tokens expire after 1 hour. Set up auto-refresh:

```javascript
auth.onIdTokenChanged(async (user) => {
  if (user) {
    const idToken = await user.getIdToken();
    console.log('🔄 Token refreshed');
    // Update your API client
  }
});
```

---

## 📡 API Client Class

```javascript
class LoneprocessAPI {
  constructor(auth) {
    this.auth = auth;
    this.baseURL = 'http://localhost:8000';
  }

  async getIdToken() {
    const user = this.auth.currentUser;
    if (!user) throw new Error('Not authenticated');
    return await user.getIdToken();
  }

  async request(endpoint, options = {}) {
    const token = await this.getIdToken();
    
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers
      }
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return await response.json();
  }

  // Convenience methods
  getLoneperiods() {
    return this.request('/api/v1/loneperiods');
  }

  getActivities(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.request(`/api/v1/activities?${params}`);
  }

  getEmployees(limit = 100) {
    return this.request(`/api/v1/la/employees?limit=${limit}`);
  }
}

// Usage
const api = new LoneprocessAPI(auth);
const periods = await api.getLoneperiods();
```

---

## ⚠️ Error Handling

```javascript
try {
  const periods = await api.getLoneperiods();
} catch (error) {
  if (error.message.includes('401')) {
    // Token expired - re-authenticate
    await signInWithCustomToken(auth, customToken);
  } else if (error.message.includes('429')) {
    // Rate limited - wait
    await new Promise(r => setTimeout(r, 1000));
  } else {
    console.error('API Error:', error);
  }
}
```

---

## 🚀 Best Practices

1. **Cache tokens** - Don't request new tokens on every call
2. **Implement retry logic** - For transient errors
3. **Use environment variables** - Never commit tokens
4. **Monitor token expiration** - Refresh proactively
5. **Handle rate limits** - Implement backoff

---

## 📊 Rate Limits

- **100 requests/minute** per token
- **50,000 reads/day** (Firebase free tier)
- HTTP 429 when exceeded

---

## 💬 Support

Need help? Contact: carl.gerhardsson@cgi.com
