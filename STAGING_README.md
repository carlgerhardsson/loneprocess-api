# Löneprocess Digital Checklista API - Staging

**Firebase + Cloud Run Staging Environment** 🎉

---

## 🔄 **QUICK START/STOP (Cost Control)**

### ⏸️ **PAUSE API ($0/month):**
1. Go to: https://console.cloud.google.com/run?project=loneprocess-api-staging
2. Click **Services** in left menu
3. Select `loneprocess-api` checkbox → Click **DELETE**
4. ✅ Confirm → **$0 cost starts immediately!**

### ▶️ **START API (5 min):**
**Option 1 - Ask Claude:**
```
"Deploy the staging API"
```

**Option 2 - GitHub UI:**
1. Go to: https://github.com/carlgerhardsson/loneprocess-api/actions
2. Click "Deploy to Cloud Run" → Select latest successful run
3. Click "Re-run all jobs"

**Option 3 - Git Push:**
```bash
git commit --allow-empty -m "chore: Redeploy"
git push origin staging
```

📚 **Full Guide:** [DELETE_DEPLOY_WORKFLOW.md](DELETE_DEPLOY_WORKFLOW.md)

**Cost:** $2-3/month when running, $0 when paused

---

## 🚀 **LIVE URL**

**Production-ready staging API:**
```
https://loneprocess-api-922770673146.us-central1.run.app
```

**Interactive API Docs (Swagger):**
```
https://loneprocess-api-922770673146.us-central1.run.app/docs
```

**Health Check:**
```
https://loneprocess-api-922770673146.us-central1.run.app/health
```

**⚠️ Important:** URL stays the same even after delete/redeploy!

---

## 🔐 **API KEYS**

All API endpoints require `X-API-Key` header.

**Example:**
```bash
curl -H "X-API-Key: YOUR_KEY" https://loneprocess-api-922770673146.us-central1.run.app/api/v1/activities
```

**Get your API key:** See [API_KEYS.md](API_KEYS.md)

---

## 🔥 Technology Stack

- **Backend:** FastAPI + Python 3.11
- **Database:** Firestore (Firebase)
- **Deployment:** Cloud Run (auto-deploy via GitHub Actions)
- **Authentication:** API Key (X-API-Key header)
- **Rate Limiting:** 60 requests/minute per IP

## 💰 Cost Control

- **Active (Min=0, Max=10):** ~$2-3/month
- **Paused (Deleted):** $0/month
- **Rate limit:** 60 req/min (protects against spikes)
- **Budget alert:** $5/month
- **Free tier:** 2M requests/month

**Recommended:** Delete when not actively testing!

## 🔄 Automatic Deployment

Every push to `staging` branch triggers automatic deployment to Cloud Run.

**Check deployment status:** https://github.com/carlgerhardsson/loneprocess-api/actions

## ✅ Setup Complete

### APIs Enabled
- ✅ Cloud Run API
- ✅ Cloud Build API  
- ✅ Artifact Registry API
- ✅ Firestore API

### Resources Created
- ✅ Artifact Registry Repository
- ✅ Firestore Database (seeded with test data)
- ✅ Cloud Run Service

### Service Account Permissions
**github-actions@loneprocess-api-staging.iam.gserviceaccount.com:**
- ✅ Cloud Run Admin
- ✅ Storage Admin
- ✅ Service Account User
- ✅ Artifact Registry Writer

**Compute Service Account (Cloud Run):**
- ✅ Cloud Datastore User (for Firestore access)

### Critical Fixes Applied
- ✅ Lazy Firebase initialization (prevents import-time crashes)
- ✅ Application Default Credentials (ADC) support
- ✅ Docker container optimized for Cloud Run
- ✅ Rate limiting middleware
- ✅ API key authentication

## 🎯 Quick Start for Frontend Teams

**1. Get your API key:**
Contact: carl.gerhardsson@cgi.com

**2. Test the API:**
```bash
curl -H "X-API-Key: YOUR_KEY" https://loneprocess-api-922770673146.us-central1.run.app/health
```

**3. Explore the API:**
Visit: https://loneprocess-api-922770673146.us-central1.run.app/docs

**4. Read integration guide:**
See: [API_KEYS.md](API_KEYS.md)

## 📊 Rate Limiting

**IMPORTANT:** This staging environment is rate-limited to protect costs.

- **Limit:** 60 requests per minute per IP address
- **Response when exceeded:** `429 Too Many Requests`
- **Header:** `X-RateLimit-Remaining` shows requests left

**For production use without limits**, contact the API team.

## 🔐 Security

- ✅ API key authentication required (X-API-Key header)
- ✅ HTTPS only (enforced by Cloud Run)
- ✅ CORS enabled for approved frontend domains
- ✅ Rate limiting prevents abuse
- ✅ Firebase Admin SDK for Firestore access

**Security Guide:** [SECURITY.md](SECURITY.md)

## 📚 Documentation

- **API Documentation:** https://loneprocess-api-922770673146.us-central1.run.app/docs
- **API Keys Guide:** [API_KEYS.md](API_KEYS.md)
- **Delete/Deploy Workflow:** [DELETE_DEPLOY_WORKFLOW.md](DELETE_DEPLOY_WORKFLOW.md)
- **Security Guide:** [SECURITY.md](SECURITY.md)
- **Pause/Resume Guide:** [PAUSE_DEPLOYMENT.md](PAUSE_DEPLOYMENT.md)

## 🐛 Issues & Support

**Report issues:** https://github.com/carlgerhardsson/loneprocess-api/issues

**Contact:** carl.gerhardsson@cgi.com

---

**Status:** 🟢 **LIVE and ready for integration!**

**Last deployed:** Auto-deployed via GitHub Actions  
**Deployment logs:** https://github.com/carlgerhardsson/loneprocess-api/actions  
**Version:** 3.0.1-staging
