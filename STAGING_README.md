# Löneprocess Digital Checklista API - Staging

**Firebase + Cloud Run Staging Environment**

## 🚀 Live URL

Once deployed: `https://loneprocess-api-[hash].run.app`

## 🔥 Technology Stack

- **Backend:** FastAPI + Python 3.11
- **Database:** Firestore (Firebase)
- **Deployment:** Cloud Run (auto-deploy via GitHub Actions)
- **Rate Limiting:** 60 requests/minute
- **Authentication:** Firebase Auth

## 💰 Cost Control

- **Max instances:** 10
- **Rate limit:** 60 req/min
- **Budget alert:** $5/month
- **Free tier:** 2M requests/month
- **Expected cost:** $0/month

## 🔄 Automatic Deployment

Every push to `staging` branch triggers automatic deployment to Cloud Run.

Check deployment status: https://github.com/carlgerhardsson/loneprocess-api/actions

## ✅ Setup Complete

- Cloud Run API ✅
- Cloud Build API ✅  
- Artifact Registry API ✅
- Artifact Registry Repository ✅
- Service Account Permissions ✅
  - Cloud Run Admin
  - Storage Admin
  - Service Account User
  - **Artifact Registry Writer**

---

**Status:** 🚀 Ready for deployment!
