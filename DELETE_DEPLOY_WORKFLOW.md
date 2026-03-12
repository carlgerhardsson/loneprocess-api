# 🔄 Delete/Deploy Workflow - $0 Cost Strategy

## 💰 Problemet

**Cloud Run kostar ~$2-3/månad även när ingen använder API:et:**
- Google tillåter inte Max instances = 0
- Containers hålls "warm" för snabbare response
- Detta kostar pengar även utan requests

**Lösningen:** DELETE service när du inte använder den, deploy när du behöver.

---

## ✅ **WORKFLOW ÖVERSIKT**

```
┌─────────────────────────────────────────────────┐
│  VECKOSTART (Måndag morgon)                     │
│  ↓                                              │
│  Deploy API (5 min) → Kostnad börjar            │
│  ↓                                              │
│  Använd hela veckan för testing                 │
│  ↓                                              │
│  VECKOSLUT (Fredag kväll)                       │
│  ↓                                              │
│  Delete API (2 min) → Kostnad slutar            │
│  ↓                                              │
│  Helg: $0 kostnad                               │
└─────────────────────────────────────────────────┘

Kostnad per månad: ~$0.50-1.00 (4 veckor × 5 dagar)
Besparing: ~65% jämfört med always-on
```

---

## 🗑️ **STEG 1: PAUSA API:et (DELETE SERVICE)**

### Via Google Cloud Console (Enklast)

**1. Gå till Cloud Run Console:**
```
https://console.cloud.google.com/run?project=loneprocess-api-staging
```

**2. Hitta din service:**
- Du ser `loneprocess-api` i listan

**3. Delete:**
- Markera checkbox bredvid `loneprocess-api`
- Klicka **DELETE** (papperskorgen) i menyn högst upp
- Bekräfta med "DELETE" i dialogen

**Resultat:**
```
✅ Service deletad
✅ $0 kostnad börjar NU
✅ URL fungerar inte längre (förväntat)
⏱️ Tar: 30 sekunder
```

---

### Via gcloud CLI (För avancerade användare)

**Om du har gcloud installerat:**

```bash
# Logga in
gcloud auth login

# Sätt projekt
gcloud config set project loneprocess-api-staging

# Delete service
gcloud run services delete loneprocess-api --region=us-central1 --quiet
```

**Resultat:**
```
✅ Deleted service [loneprocess-api]
```

---

## 🚀 **STEG 2: STARTA API:et IGEN (DEPLOY)**

### Metod 1: Via Git Push (Rekommenderat)

**I din terminal:**

```powershell
# Gå till projekt-mappen
cd "H:\Filer från gamla datorn 2\Filer från gamla\Eget labbande med Visual Studio Agenter\loneprocess-api"

# Säkerställ du är på staging branch
git checkout staging

# Gör en tom commit (triggar deployment)
git commit --allow-empty -m "chore: Redeploy API to Cloud Run"

# Push till GitHub
git push origin staging
```

**Resultat:**
```
✅ GitHub Actions startar automatiskt
✅ Bygger Docker image
✅ Pushar till Artifact Registry
✅ Deployer till Cloud Run
✅ API live igen efter ~5 minuter
```

---

### Metod 2: Via GitHub Actions UI (Ingen Git krävs)

**1. Gå till GitHub Actions:**
```
https://github.com/carlgerhardsson/loneprocess-api/actions
```

**2. Välj workflow:**
- Klicka på "Deploy to Cloud Run" i vänstermenyn

**3. Välj senaste successful run:**
- Du ser en lista med tidigare deployments
- Välj den senaste som lyckades (grön checkmark)

**4. Re-run:**
- Klicka "Re-run all jobs" (högst upp till höger)
- Bekräfta

**Resultat:**
```
✅ Deployment startar
✅ Samma resultat som git push
✅ API live efter ~5 minuter
```

---

### Metod 3: Via gcloud CLI (Snabbast för repeat deployments)

**Om du har gcloud installerat:**

```bash
# Logga in
gcloud auth login

# Sätt projekt
gcloud config set project loneprocess-api-staging

# Deploy senaste image
gcloud run deploy loneprocess-api \
  --image us-central1-docker.pkg.dev/loneprocess-api-staging/loneprocess-api/loneprocess-api:latest \
  --region us-central1 \
  --allow-unauthenticated \
  --max-instances 10 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 60s
```

**Resultat:**
```
✅ API live efter ~2 minuter (snabbare än GitHub Actions)
```

---

## ✅ **STEG 3: VERIFIERA ATT API:et ÄR LIVE**

**Efter deployment, testa:**

```powershell
# Health check (ingen API key)
iwr "https://loneprocess-api-922770673146.us-central1.run.app/health"

# Med API key
iwr "https://loneprocess-api-922770673146.us-central1.run.app/api/v1/activities" -Headers @{"X-API-Key"="wXWoaJ13LTuPVcxqmzLYFKz9euJw_h4V7PkWnEfvONs"}
```

**Förväntat:**
```
StatusCode: 200
Content: {"status":"healthy",...}
```

---

## 📅 **EXEMPEL ANVÄNDNINGSSCENARIO**

### **Sprint-baserad användning (2 veckor):**

```
Vecka 1 (Sprint start):
├─ Måndag 09:00: Deploy API (git push)
├─ Må-Fre: Frontend team utvecklar och testar
└─ Fredag 17:00: Delete API

Helg: $0 kostnad

Vecka 2 (Sprint fortsättning):
├─ Måndag 09:00: Deploy API (git push)
├─ Må-Fre: Fortsatt testning
└─ Fredag 17:00: Delete API (sprint slut)

Kostnad totalt: ~$1.20 (10 dagar × ~$0.12/dag)
Besparing: ~$4-5 jämfört med always-on
```

---

### **Ad-hoc testning:**

```
Tisdag 14:00:
├─ "Behöver testa något"
├─ Deploy API (5 min)
├─ Testa i 2 timmar
└─ Delete API

Kostnad: ~$0.01 (2 timmar × $0.005/timme)
```

---

## 🎯 **BEST PRACTICES**

### ✅ **GÖR:**

1. **Planera dina test-sessioner**
   - Deploy inför sprint/demo
   - Delete efter varje arbetsdag/vecka

2. **Kommunicera med teamet**
   - Meddela när API:et är live/pausat
   - Använd Slack/Teams för notifikationer

3. **Använd GitHub Actions**
   - Enklaste sättet att re-deploy
   - Full traceability i Git history

4. **Kolla logs innan delete**
   - Verifiera att inga error har uppstått
   - Spara viktiga logs om behövs

### ❌ **UNDVIK:**

1. **Glömma att delete**
   - Sätt påminnelser (Outlook/Calendar)
   - Kostnad fortsätter annars

2. **Deploy mitt i natten**
   - Ingen använder API:et ändå
   - Onödig kostnad

3. **För många deployments**
   - Varje deploy tar 5 min
   - Planera istället för ad-hoc

---

## 💡 **AUTOMATIONS-TIPS**

### **PowerShell Script för Delete:**

```powershell
# save as: pause-api.ps1

Write-Host "🗑️ Pausar loneprocess-api..." -ForegroundColor Yellow

gcloud run services delete loneprocess-api `
  --region=us-central1 `
  --project=loneprocess-api-staging `
  --quiet

Write-Host "✅ API pausat! $0 kostnad nu." -ForegroundColor Green
```

**Använd:**
```powershell
.\pause-api.ps1
```

---

### **PowerShell Script för Deploy:**

```powershell
# save as: deploy-api.ps1

Write-Host "🚀 Startar loneprocess-api deployment..." -ForegroundColor Yellow

cd "H:\Filer från gamla datorn 2\Filer från gamla\Eget labbande med Visual Studio Agenter\loneprocess-api"

git checkout staging
git commit --allow-empty -m "chore: Redeploy API"
git push origin staging

Write-Host "⏳ Deployment startad! Klar om ~5 min." -ForegroundColor Green
Write-Host "📊 Status: https://github.com/carlgerhardsson/loneprocess-api/actions" -ForegroundColor Cyan
```

**Använd:**
```powershell
.\deploy-api.ps1
```

---

## 📊 **KOSTNADSJÄMFÖRELSE**

| Scenario | Dagar/månad | Kostnad/månad |
|----------|-------------|---------------|
| **Always-on** | 30 | **$2-3** |
| **5-day workweek** | 20 | **$1.30-2.00** |
| **Sprint-based (2×5 days)** | 10 | **$0.65-1.00** |
| **Ad-hoc (totalt 5 dagar)** | 5 | **$0.35-0.50** |
| **Deleted** | 0 | **$0.00** |

---

## ⚠️ **VIKTIGT ATT VETA**

### **Data försvinner INTE:**
- ✅ Firestore data finns kvar (alltid)
- ✅ GitHub code finns kvar
- ✅ Docker images finns kvar i Artifact Registry
- ✅ API keys fungerar direkt efter re-deploy

### **Vad försvinner:**
- ❌ Cloud Run service (själva containern)
- ❌ Service URL slutar fungera
- ❌ Logs för servicen (sparas i 30 dagar)

### **Re-deploy:**
- ⏱️ Tar 5 minuter (GitHub Actions)
- ⏱️ Tar 2 minuter (gcloud CLI)
- ✅ Samma URL återkommer
- ✅ Samma konfiguration

---

## 🎓 **LÄRANDE KURVA**

**Första gången:**
- 📚 Läs denna guide: 10 min
- 🧪 Testa delete/deploy: 15 min
- 📝 Skapa egna scripts: 20 min

**Därefter:**
- ⚡ Delete: 30 sekunder
- ⚡ Deploy: 1 minut (+ vänta 5 min)
- ⚡ Total tid: ~6 minuter per cykel

---

## 📞 **SUPPORT**

**Problem med delete/deploy?**

**Scenario 1: "Deployment failar"**
- Kolla GitHub Actions logs
- Vanligaste: Docker build error
- Lösning: Kolla senaste commit

**Scenario 2: "API svarar inte efter deploy"**
- Vänta 5 minuter (deployment tar tid)
- Kolla Cloud Run logs
- Verifiera med /health endpoint

**Scenario 3: "Glömt deleta, kostat pengar"**
- Delete omedelbart
- Kostnad: ~$0.10 per extra dag
- Sätt kalender-påminnelse framöver

**Kontakt:** carl.gerhardsson@cgi.com

---

## ✅ **SAMMANFATTNING**

**Delete/Deploy workflow ger:**
- 💰 **65-100% kostnadsbesparing** ($0-1/månad vs $2-3/månad)
- ⚡ **Snabb re-deployment** (5 min via GitHub Actions)
- 🔒 **Ingen data-förlust** (Firestore bevaras)
- 🎯 **Full kontroll** över när API:et körs

**Perfekt för:**
- ✅ Staging/test-miljöer
- ✅ Sprint-baserad utveckling
- ✅ Intermittent användning
- ✅ Cost-conscious teams

**Inte för:**
- ❌ Production (ska alltid vara live)
- ❌ 24/7 monitoring behövs
- ❌ External SLA commitments

---

**Senast uppdaterad:** 2026-03-12  
**Status:** ✅ Verifierad och testad
