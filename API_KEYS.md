# 🔐 API Keys - Staging Environment

## 📋 Active API Keys

### Frontend Team X
```
Key: wXWoaJ13LTuPVcxqmzLYFKz9euJw_h4V7PkWnEfvONs
Team: Frontend Team X
Purpose: Frontend integration and testing
Issued: 2026-03-12
```

### Internal Dev Team
```
Key: zXb_f7MYOeXdnPe6iQPc7VrD1pMH5AC388AM1YfFdyc
Team: Internal Dev Team  
Purpose: Backend development and testing
Issued: 2026-03-12
```

### Testing/QA
```
Key: BptF6lJZqhynSameW-OiNtLodKt3tsi0IPSukpV8nxA
Team: Testing/QA
Purpose: Automated tests and QA validation
Issued: 2026-03-12
```

---

## 🔑 How to Use API Keys

### With cURL:
```bash
curl -H "X-API-Key: wXWoaJ13LTuPVcxqmzLYFKz9euJw_h4V7PkWnEfvONs" \
  https://loneprocess-api-922770673146.us-central1.run.app/api/v1/activities
```

### With JavaScript (fetch):
```javascript
fetch('https://loneprocess-api-922770673146.us-central1.run.app/api/v1/activities', {
  headers: {
    'X-API-Key': 'wXWoaJ13LTuPVcxqmzLYFKz9euJw_h4V7PkWnEfvONs'
  }
})
.then(res => res.json())
.then(data => console.log(data));
```

### With Python (requests):
```python
import requests

headers = {
    'X-API-Key': 'wXWoaJ13LTuPVcxqmzLYFKz9euJw_h4V7PkWnEfvONs'
}

response = requests.get(
    'https://loneprocess-api-922770673146.us-central1.run.app/api/v1/activities',
    headers=headers
)

data = response.json()
```

---

## ⚠️ Security Guidelines

**DO:**
- ✅ Store keys in environment variables
- ✅ Use HTTPS only (enforced by Cloud Run)
- ✅ Rotate keys periodically
- ✅ Use different keys per team/environment
- ✅ Report compromised keys immediately

**DON'T:**
- ❌ Commit keys to Git repositories
- ❌ Share keys via email/Slack
- ❌ Hardcode keys in frontend code
- ❌ Use the same key across environments
- ❌ Share your key with unauthorized people

---

## 🔄 Key Management

### To Add a New Key:

1. Generate a secure key:
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. Add to `api_keys.py`:
   ```python
   API_KEYS = {
       "new_key_here": "New Team Name",
       # ... existing keys
   }
   ```

3. Deploy to staging:
   ```bash
   git add api_keys.py
   git commit -m "feat: Add API key for New Team"
   git push
   ```

### To Revoke a Key:

1. Remove from `api_keys.py`
2. Deploy to staging
3. Notify affected team

**OR** use programmatic revocation:
```python
from api_keys import revoke_key
revoke_key("key_to_revoke")
```

---

## 📊 Monitoring

**View API key usage in Cloud Logs:**
```
https://console.cloud.google.com/run/detail/us-central1/loneprocess-api/logs?project=loneprocess-api-staging
```

**Filter by team:**
```
resource.type="cloud_run_revision"
jsonPayload.message=~"Frontend Team X"
```

---

## 🚨 If a Key is Compromised

1. **Immediately revoke** the key in `api_keys.py`
2. **Deploy** the change (takes ~5 min)
3. **Generate new key** for the affected team
4. **Notify** the team via secure channel
5. **Investigate** logs for suspicious activity

---

## 📞 Support

**Need a new key or have questions?**
- Contact: carl.gerhardsson@cgi.com
- Create issue: https://github.com/carlgerhardsson/loneprocess-api/issues

---

**Last updated:** 2026-03-12
**Status:** 🟢 Active with 3 registered teams
