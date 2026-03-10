# Firebase Authentication Setup

How to authenticate with the Löneprocess API using Firebase.

---

## 📦 Installation

### JavaScript/Node.js

```bash
npm install firebase
```

### Python (Server-side)

```bash
pip install firebase-admin
```

---

## 🔧 Configuration

You'll receive these from your API administrator:

```javascript
const firebaseConfig = {
  apiKey: "Contact admin for this",
  authDomain: "loneprocess-api-staging.firebaseapp.com",
  projectId: "loneprocess-api-staging"
};
```

---

## 🔑 Custom Token Authentication

### JavaScript Example

```javascript
import { initializeApp } from 'firebase/app';
import { getAuth, signInWithCustomToken } from 'firebase/auth';

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Your custom token from admin
const customToken = 'YOUR_CUSTOM_TOKEN';

async function authenticate() {
  try {
    const userCredential = await signInWithCustomToken(auth, customToken);
    const idToken = await userCredential.user.getIdToken();
    
    console.log('✅ Authenticated!', idToken);
    return idToken;
  } catch (error) {
    console.error('❌ Error:', error.code, error.message);
  }
}
```

---

## 🔄 Token Lifecycle

### Flow:

```
1. Admin generates custom token → [Custom Token]
2. Client exchanges for ID token → [ID Token] (expires 1h)
3. Use ID token in API calls → [API Access]
4. Token expires → [Auto-refresh]
5. Get new ID token → [API Access]
```

### Auto-Refresh:

```javascript
auth.onIdTokenChanged(async (user) => {
  if (user) {
    const idToken = await user.getIdToken();
    console.log('🔄 Token refreshed');
  }
});
```

---

## 🛡️ Security Best Practices

### ✅ DO:
- Store tokens in environment variables
- Implement token refresh logic
- Use HTTPS only
- Handle expiration gracefully

### ❌ DON'T:
- Commit tokens to Git
- Share tokens between teams
- Expose tokens in client code
- Ignore token expiration

---

## 🐛 Troubleshooting

### "INVALID_CUSTOM_TOKEN"
**Solution:** Token expired or malformed. Request new token.

### "TOKEN_EXPIRED"
**Solution:** ID token expired (1h). Use refresh token.

### "PERMISSION_DENIED"
**Solution:** Missing required claims. Verify team claim.

---

## 💬 Support

Contact: carl.gerhardsson@cgi.com
