# Löneprocess Digital Checklista API - Staging

**Firebase + Cloud Run Staging Environment** 🎉

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

## 🔥 Technology Stack

- **Backend:** FastAPI + Python 3.11
- **Database:** Firestore (Firebase)
- **Deployment:** Cloud Run (auto-deploy via GitHub Actions)
- **Rate Limiting:** 60 requests/minute per IP
- **Authentication:** Firebase Auth ready

## 💰 Cost Control

- **Max instances:** 10
- **Rate limit:** 60 req/min
- **Budget alert:** $5/month
- **Free tier:** 2M requests/month
- **Expected cost:** $0/month (within free tier)

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

## 🎯 Quick Start for Frontend Teams

**1. Test the API:**
```bash
curl https://loneprocess-api-922770673146.us-central1.run.app/health
```

**2. Explore the API:**
Visit: https://loneprocess-api-922770673146.us-central1.run.app/docs

**3. Get your API token:**
Contact: carl.gerhardsson@cgi.com

**4. Read integration guide:**
See: https://github.com/carlgerhardsson/loneprocess-api-docs

## 📊 Rate Limiting

**IMPORTANT:** This staging environment is rate-limited to protect costs.

- **Limit:** 60 requests per minute per IP address
- **Response when exceeded:** `429 Too Many Requests`
- **Header:** `X-RateLimit-Remaining` shows requests left

**For production use without limits**, contact the API team.

## 🔐 Security

- All requests require valid Firebase authentication token
- HTTPS only (enforced by Cloud Run)
- CORS enabled for approved frontend domains
- Rate limiting prevents abuse

## 📚 Documentation

- **API Documentation:** https://loneprocess-api-922770673146.us-central1.run.app/docs
- **Integration Guide:** https://github.com/carlgerhardsson/loneprocess-api-docs
- **Example Code:** https://github.com/carlgerhardsson/loneprocess-api-docs/tree/main/examples

## 🐛 Issues & Support

**Report issues:** https://github.com/carlgerhardsson/loneprocess-api/issues

**Contact:** carl.gerhardsson@cgi.com

---

**Status:** 🟢 **LIVE and ready for integration!**

**Last deployed:** Auto-deployed via GitHub Actions
**Deployment logs:** https://github.com/carlgerhardsson/loneprocess-api/actions
