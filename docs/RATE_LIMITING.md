# Rate Limiting Policy

**API kostnadskontroll och användarbegränsningar**

---

## 🛡️ Rate Limits

### **Aktuella begränsningar:**

| Limit Type | Value | Window | Scope |
|------------|-------|--------|-------|
| **Requests** | 60 | 1 minute | Per IP address |
| **Burst** | 60 | 1 minute | Per IP address |

**I klartext:**
- Max **60 requests per minut** per IP-adress
- Genomsnitt: **1 request per sekund**
- Burst tillåtet: Ja, upp till 60 requests direkt

---

## 🚨 Vad händer vid överskridande?

### **HTTP 429 - Too Many Requests**

```json
{
  "detail": {
    "error": "Rate limit exceeded",
    "message": "Maximum 60 requests per minute allowed",
    "retry_after": 60,
    "limit": 60,
    "window": "1 minute"
  }
}
```

**Response Headers:**
```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1678901234
Retry-After: 60
```

---

## ✅ Best Practices för Frontend

### **1. Implementera Retry Logic**

```javascript
async function apiCallWithRetry(url, options, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url, options);
      
      if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After') || 60;
        console.log(`Rate limited. Waiting ${retryAfter}s...`);
        await new Promise(r => setTimeout(r, retryAfter * 1000));
        continue;
      }
      
      return response;
    } catch (error) {
      if (i === maxRetries - 1) throw error;
    }
  }
}
```

### **2. Kolla Rate Limit Headers**

```javascript
const response = await fetch(url, options);

const remaining = response.headers.get('X-RateLimit-Remaining');
const limit = response.headers.get('X-RateLimit-Limit');

if (remaining < 10) {
  console.warn(`⚠️ Only ${remaining}/${limit} requests left this minute`);
}
```

### **3. Implementera Client-Side Throttling**

```javascript
// Throttle to max 1 request/second
const throttle = (func, delay) => {
  let lastCall = 0;
  return async (...args) => {
    const now = Date.now();
    const timeSinceLastCall = now - lastCall;
    
    if (timeSinceLastCall < delay) {
      await new Promise(r => setTimeout(r, delay - timeSinceLastCall));
    }
    
    lastCall = Date.now();
    return func(...args);
  };
};

// Usage
const throttledFetch = throttle(fetch, 1000); // 1 request/second
```

### **4. Batch Requests

```javascript
// BAD - 100 separate requests
for (const id of employeeIds) {
  await fetch(`/api/v1/employees/${id}`);
}

// GOOD - 1 request with filtering
const employees = await fetch('/api/v1/employees?limit=100');
```

---

## 💰 Varför Rate Limiting?

### **Kostnadskontroll:**

Firebase Cloud Functions kostar per:
- **Invocation:** $0.40 per 1M requests
- **Compute:** $0.0000025 per GB-second
- **Networking:** $0.12 per GB

**Med 60 req/min limit:**
```
Max användning per månad:
60 req/min × 60 min × 24 h × 30 days = 2,592,000 requests

Kostnad:
2.5M requests × $0.40/1M = $1.00/månad
```

**Free Tier täcker:** 2M requests/månad = **$0 kostnad**

---

## 📊 Monitoring

### **Kolla din användning:**

```javascript
// API returnerar rate limit info i varje response
const response = await fetch('/api/v1/loneperiods');

console.log('Limit:', response.headers.get('X-RateLimit-Limit'));
console.log('Remaining:', response.headers.get('X-RateLimit-Remaining'));
console.log('Reset:', new Date(response.headers.get('X-RateLimit-Reset') * 1000));
```

### **Firebase Console:**

Monitorera användning här:
- https://console.firebase.google.com/project/loneprocess-api-staging/usage

---

## ⚠️ Vanliga Misstag

### **1. Polling i tight loop**
```javascript
// ❌ BAD - Når limit på 60 sekunder
while (true) {
  await fetch('/api/v1/loneperiods/202501');
}

// ✅ GOOD - Poll var 5:e sekund
setInterval(async () => {
  await fetch('/api/v1/loneperiods/202501');
}, 5000);
```

### **2. Ingen error handling**
```javascript
// ❌ BAD - Crashar vid 429
const data = await fetch(url).then(r => r.json());

// ✅ GOOD - Hanterar 429
try {
  const response = await fetch(url);
  if (response.status === 429) {
    // Handle rate limit
  }
  const data = await response.json();
} catch (error) {
  console.error('API error:', error);
}
```

### **3. Parallella requests utan kontroll**
```javascript
// ❌ BAD - 100 requests på en gång
const promises = ids.map(id => fetch(`/api/v1/employees/${id}`));
await Promise.all(promises);

// ✅ GOOD - Batch med rate limit awareness
for (const batch of chunk(ids, 10)) {
  await Promise.all(batch.map(id => fetch(`/api/v1/employees/${id}`)));
  await new Promise(r => setTimeout(r, 10000)); // Vänta 10s mellan batches
}
```

---

## 🎯 Rekommendationer

### **För normal användning:**
- ✅ Max 1 request per sekund är säkert
- ✅ Använd throttling/debouncing
- ✅ Cacha data där möjligt
- ✅ Implementera retry logic

### **För development/testing:**
- ✅ Testa med verkliga delays (inte tight loops)
- ✅ Övervaka rate limit headers
- ✅ Logga 429 responses

### **För production:**
- ✅ Implementera exponential backoff
- ✅ Använd request queuing
- ✅ Monitrera användning dagligen

---

## 📞 Support

Om rate limits är för låga för ditt use case:
- **Email:** carl.gerhardsson@cgi.com
- **Motivera:** Förklara ditt behov
- **Lösning:** Vi kan justera limits vid behov

---

**Uppdaterad:** 2026-03-11  
**Gäller för:** API v3.0 Staging  
**Review:** Vid behov
