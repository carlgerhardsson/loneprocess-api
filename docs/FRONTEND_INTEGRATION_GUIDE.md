# 🚀 Frontend Integration Guide

**Löneprocess Digital Checklista API**  
**Version:** 3.0.1-staging  
**Last Updated:** 2026-03-15

---

## 📋 Table of Contents

1. [Quick Start (5 minutes)](#quick-start-5-minutes)
2. [Authentication](#authentication)
3. [Base URL & Endpoints](#base-url--endpoints)
4. [Code Examples](#code-examples)
5. [Error Handling](#error-handling)
6. [Rate Limits](#rate-limits)
7. [TypeScript Support](#typescript-support)
8. [Testing](#testing)
9. [Best Practices](#best-practices)
10. [Support](#support)

---

## ⚡ Quick Start (5 minutes)

### Step 1: Get Your API Key

Your API key has been provided separately via secure channel.

```bash
# Store in environment variable (recommended)
export LONEPROCESS_API_KEY="your-api-key-here"
```

### Step 2: Test the Connection

```bash
curl -H "X-API-Key: $LONEPROCESS_API_KEY" \
  https://loneprocess-api-922770673146.us-central1.run.app/api/v1/activities
```

**Expected response:** `200 OK` with JSON array of activities.

### Step 3: Explore the API

Open interactive documentation:
```
https://loneprocess-api-922770673146.us-central1.run.app/docs
```

You can test all endpoints directly in your browser!

---

## 🔐 Authentication

### API Key Header

All requests require the `X-API-Key` header:

```http
GET /api/v1/activities HTTP/1.1
Host: loneprocess-api-922770673146.us-central1.run.app
X-API-Key: your-api-key-here
```

### Security Best Practices

**✅ DO:**
- Store API key in environment variables
- Use `.env` files (add to `.gitignore`)
- Rotate keys periodically
- Use HTTPS only (enforced by default)

**❌ DON'T:**
- Hardcode keys in source code
- Commit keys to version control
- Share keys in plain text (email, Slack)
- Expose keys in client-side code

---

## 🌐 Base URL & Endpoints

### Base URL
```
https://loneprocess-api-922770673146.us-central1.run.app
```

### Main Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check (no auth required) |
| `/api/v1/activities` | GET | List all activities |
| `/api/v1/activities/{id}` | GET | Get specific activity |
| `/api/v1/activities` | POST | Create activity |
| `/api/v1/activities/{id}` | PUT | Update activity |
| `/api/v1/activities/{id}` | DELETE | Delete activity |
| `/api/v1/loneperiods` | GET | List payroll periods |
| `/api/v1/loneperiods/{id}` | GET | Get specific period |

See [API_EXAMPLES.md](../API_EXAMPLES.md) for complete endpoint list.

---

## 💻 Code Examples

### React + TypeScript

```typescript
// hooks/useAPI.ts
import { useState, useEffect } from 'react';

const API_BASE = 'https://loneprocess-api-922770673146.us-central1.run.app';
const API_KEY = process.env.REACT_APP_LONEPROCESS_API_KEY;

interface Activity {
  id: number;
  namn: string;
  beskrivning: string;
  ansvarig: string;
  status: 'ej_startad' | 'pagaende' | 'slutford';
}

export function useActivities() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function fetchActivities() {
      try {
        const response = await fetch(`${API_BASE}/api/v1/activities`, {
          headers: {
            'X-API-Key': API_KEY!,
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        setActivities(data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Unknown error'));
      } finally {
        setLoading(false);
      }
    }

    fetchActivities();
  }, []);

  return { activities, loading, error };
}
```

**Usage:**
```typescript
import { useActivities } from './hooks/useAPI';

function ActivitiesList() {
  const { activities, loading, error } = useActivities();

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {activities.map(activity => (
        <li key={activity.id}>{activity.namn}</li>
      ))}
    </ul>
  );
}
```

---

### Vue 3 + Composition API

```typescript
// composables/useAPI.ts
import { ref } from 'vue';

const API_BASE = 'https://loneprocess-api-922770673146.us-central1.run.app';
const API_KEY = import.meta.env.VITE_LONEPROCESS_API_KEY;

export function useActivities() {
  const activities = ref([]);
  const loading = ref(true);
  const error = ref(null);

  async function fetchActivities() {
    try {
      const response = await fetch(`${API_BASE}/api/v1/activities`, {
        headers: {
          'X-API-Key': API_KEY,
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      activities.value = await response.json();
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  }

  fetchActivities();

  return { activities, loading, error };
}
```

**Usage:**
```vue
<script setup lang="ts">
import { useActivities } from '@/composables/useAPI';

const { activities, loading, error } = useActivities();
</script>

<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">Error: {{ error }}</div>
  <ul v-else>
    <li v-for="activity in activities" :key="activity.id">
      {{ activity.namn }}
    </li>
  </ul>
</template>
```

---

### Vanilla JavaScript

```javascript
// api.js
const API_BASE = 'https://loneprocess-api-922770673146.us-central1.run.app';
const API_KEY = 'your-api-key-here'; // Use env var in production!

class LoneprocessAPI {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseURL = API_BASE;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      ...options,
      headers: {
        'X-API-Key': this.apiKey,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    const response = await fetch(url, config);

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: response.statusText
      }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Activities
  getActivities() {
    return this.request('/api/v1/activities');
  }

  getActivity(id) {
    return this.request(`/api/v1/activities/${id}`);
  }

  createActivity(data) {
    return this.request('/api/v1/activities', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  updateActivity(id, data) {
    return this.request(`/api/v1/activities/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  deleteActivity(id) {
    return this.request(`/api/v1/activities/${id}`, {
      method: 'DELETE',
    });
  }

  // Payroll Periods
  getLoneperiods() {
    return this.request('/api/v1/loneperiods');
  }
}

// Usage
const api = new LoneprocessAPI(API_KEY);

api.getActivities()
  .then(activities => console.log(activities))
  .catch(error => console.error(error));
```

---

## ⚠️ Error Handling

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Check request payload |
| 401 | Unauthorized | Verify API key |
| 404 | Not Found | Check endpoint URL |
| 429 | Too Many Requests | Implement retry with backoff |
| 500 | Server Error | Retry later, contact support |

### Error Response Format

```json
{
  "detail": "Missing API key. Please provide X-API-Key header."
}
```

### Handling Errors

```typescript
async function fetchWithErrorHandling(url: string) {
  try {
    const response = await fetch(url, {
      headers: { 'X-API-Key': API_KEY },
    });

    if (!response.ok) {
      // Parse error response
      const error = await response.json();
      
      switch (response.status) {
        case 401:
          // Invalid API key
          console.error('Authentication failed. Check API key.');
          break;
        case 429:
          // Rate limited
          console.error('Rate limit exceeded. Retry after 60 seconds.');
          break;
        case 500:
          // Server error
          console.error('Server error. Please try again later.');
          break;
        default:
          console.error(`Error: ${error.detail}`);
      }
      
      throw new Error(error.detail);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof TypeError) {
      // Network error
      console.error('Network error. Check your connection.');
    }
    throw error;
  }
}
```

---

## 🚦 Rate Limits

**Current limits:**
- **60 requests per minute** per IP address
- **10 max concurrent connections**

### Rate Limit Headers

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1710259200
```

### Handling Rate Limits

```typescript
async function fetchWithRetry(url: string, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url, {
        headers: { 'X-API-Key': API_KEY },
      });

      if (response.status === 429) {
        // Rate limited - wait and retry
        const retryAfter = 60; // seconds
        console.log(`Rate limited. Retrying in ${retryAfter}s...`);
        await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
        continue;
      }

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}
```

---

## 📘 TypeScript Support

### Type Definitions

```typescript
// types/loneprocess.ts

export type ActivityStatus = 'ej_startad' | 'pagaende' | 'slutford';
export type Veckodag = 'Monday' | 'Tuesday' | 'Wednesday' | 'Thursday' | 'Friday';

export interface Activity {
  id: number;
  namn: string;
  beskrivning: string;
  ansvarig: string;
  berakning_frekvens: 'daglig' | 'veckovis' | 'manatlig';
  manad_dag?: number;
  vecka_dag?: Veckodag;
  tid?: string;
  status: ActivityStatus;
  senast_utford?: string;
  created_at: string;
  updated_at: string;
}

export interface Loneperiod {
  id: number;
  period: string;
  start_datum: string;
  slut_datum: string;
  loneutbetalning_datum: string;
  status: 'planerad' | 'aktiv' | 'avslutad';
  created_at: string;
  updated_at: string;
}

export interface CreateActivityRequest {
  namn: string;
  beskrivning: string;
  ansvarig: string;
  berakning_frekvens: 'daglig' | 'veckovis' | 'manatlig';
  manad_dag?: number;
  vecka_dag?: Veckodag;
  tid?: string;
}

export interface UpdateActivityRequest extends Partial<CreateActivityRequest> {
  status?: ActivityStatus;
}

export interface APIError {
  detail: string;
}
```

---

## 🧪 Testing

### Unit Tests (Jest)

```typescript
// api.test.ts
import { LoneprocessAPI } from './api';

describe('LoneprocessAPI', () => {
  const api = new LoneprocessAPI('test-api-key');

  beforeEach(() => {
    global.fetch = jest.fn();
  });

  it('should fetch activities', async () => {
    const mockActivities = [{ id: 1, namn: 'Test' }];
    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => mockActivities,
    });

    const activities = await api.getActivities();
    expect(activities).toEqual(mockActivities);
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/activities'),
      expect.objectContaining({
        headers: expect.objectContaining({
          'X-API-Key': 'test-api-key',
        }),
      })
    );
  });

  it('should handle errors', async () => {
    (global.fetch as jest.Mock).mockResolvedValue({
      ok: false,
      status: 401,
      json: async () => ({ detail: 'Invalid API key' }),
    });

    await expect(api.getActivities()).rejects.toThrow('Invalid API key');
  });
});
```

### Integration Tests

```typescript
// integration.test.ts
describe('API Integration', () => {
  const API_KEY = process.env.TEST_API_KEY;
  const api = new LoneprocessAPI(API_KEY!);

  it('should create, read, update, and delete activity', async () => {
    // Create
    const newActivity = await api.createActivity({
      namn: 'Test Activity',
      beskrivning: 'Test',
      ansvarig: 'Tester',
      berakning_frekvens: 'daglig',
    });
    expect(newActivity.id).toBeDefined();

    // Read
    const activity = await api.getActivity(newActivity.id);
    expect(activity.namn).toBe('Test Activity');

    // Update
    const updated = await api.updateActivity(newActivity.id, {
      status: 'slutford',
    });
    expect(updated.status).toBe('slutford');

    // Delete
    await api.deleteActivity(newActivity.id);
    await expect(api.getActivity(newActivity.id)).rejects.toThrow();
  });
});
```

---

## ✨ Best Practices

### 1. Environment Variables

**React (.env):**
```bash
REACT_APP_LONEPROCESS_API_KEY=your-key-here
REACT_APP_API_BASE_URL=https://loneprocess-api-922770673146.us-central1.run.app
```

**Vue (.env):**
```bash
VITE_LONEPROCESS_API_KEY=your-key-here
VITE_API_BASE_URL=https://loneprocess-api-922770673146.us-central1.run.app
```

### 2. Request Caching

```typescript
// Simple in-memory cache
const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

async function fetchWithCache(url: string) {
  const cached = cache.get(url);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }

  const data = await fetch(url, {
    headers: { 'X-API-Key': API_KEY },
  }).then(r => r.json());

  cache.set(url, { data, timestamp: Date.now() });
  return data;
}
```

### 3. Pagination

```typescript
interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
}

async function fetchPaginated<T>(
  endpoint: string,
  page: number = 1,
  perPage: number = 20
): Promise<PaginatedResponse<T>> {
  const url = `${API_BASE}${endpoint}?page=${page}&per_page=${perPage}`;
  return fetch(url, {
    headers: { 'X-API-Key': API_KEY },
  }).then(r => r.json());
}
```

### 4. Batch Operations

```typescript
async function batchUpdate(updates: Array<{ id: number; data: any }>) {
  // Execute in parallel (respecting rate limits)
  const chunks = chunkArray(updates, 10); // 10 concurrent requests
  
  for (const chunk of chunks) {
    await Promise.all(
      chunk.map(({ id, data }) => api.updateActivity(id, data))
    );
    await new Promise(resolve => setTimeout(resolve, 1000)); // Rate limit buffer
  }
}
```

---

## 📞 Support

### Documentation

- **Swagger UI:** https://loneprocess-api-922770673146.us-central1.run.app/docs
- **API Examples:** [API_EXAMPLES.md](../API_EXAMPLES.md)
- **Security Guide:** [SECURITY.md](../SECURITY.md)
- **API Keys:** [API_KEYS.md](../API_KEYS.md)

### Contact

**Technical Support:**
- Email: carl.gerhardsson@cgi.com
- GitHub Issues: https://github.com/carlgerhardsson/loneprocess-api/issues

**Response Times:**
- Critical issues: Within 4 hours
- General questions: Within 24 hours
- Feature requests: Within 3 business days

### Reporting Issues

When reporting issues, please include:

1. **Request details:**
   - Endpoint URL
   - HTTP method
   - Request headers (mask API key!)
   - Request body

2. **Response details:**
   - HTTP status code
   - Response body
   - Error message

3. **Environment:**
   - Browser/Node.js version
   - Framework (React, Vue, etc.)
   - Timestamp of the issue

---

## 🚀 Next Steps

1. ✅ Review this guide
2. ✅ Set up your API key
3. ✅ Test the connection
4. ✅ Explore Swagger UI
5. ✅ Implement your first integration
6. ✅ Set up error handling
7. ✅ Add tests
8. ✅ Deploy to production

---

**Welcome to the Löneprocess API!** 🎉

We're excited to have you building with us. If you have any questions, don't hesitate to reach out!
