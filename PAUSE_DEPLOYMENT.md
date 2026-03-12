# 💰 Pausa och Starta API:et (Kostnadskontroll)

## 🎯 Översikt

Cloud Run kostar bara när containern kör. Genom att sätta max instances till 0 garanteras att **inga containers startar = $0 kostnad**.

**Nuvarande status:**
- ✅ Live: https://loneprocess-api-922770673146.us-central1.run.app
- 💰 Kostnad när pausad: **$0/månad**
- 💰 Kostnad när aktiv (med rate limit): **$0/månad** (inom free tier)

---

## 🔴 PAUSA API:et (Stäng av helt)

### Metod 1: Via Cloud Console (Rekommenderat)

**Steg:**

1. **Gå till Cloud Run service:**
   ```
   https://console.cloud.google.com/run/detail/us-central1/loneprocess-api?project=loneprocess-api-staging
   ```

2. **Klicka "EDIT & DEPLOY NEW REVISION"** (högst upp)

3. **Under "Revision scaling":**
   - Minimum number of instances: `0` (lämna som det är)
   - **Maximum number of instances: Ändra till `0`** ⬅️ VIKTIGT!

4. **Klicka "DEPLOY"** (längst ner)

5. **Vänta ~30 sekunder** tills deployment är klar

**Resultat:**
- ✅ API:et är **avstängt** (ger timeout/error på requests)
- ✅ **$0 kostnad** - inga containers kan starta
- ✅ All konfiguration sparad (Firestore, permissions, etc.)

---

### Metod 2: Ta bort hela servicen (Permanent borttagning)

**Varning:** Detta tar bort servicen helt. Du måste deploya igen via GitHub Actions för att starta.

**Steg:**

1. **Gå till Cloud Run:**
   ```
   https://console.cloud.google.com/run?project=loneprocess-api-staging
   ```

2. **Markera checkbox** bredvid `loneprocess-api`

3. **Klicka "DELETE"** (papperskorgen i menyn)

4. **Bekräfta borttagning**

**Resultat:**
- ✅ **$0 kostnad** - servicen finns inte
- ❌ URL:en fungerar inte alls
- ⚠️ Måste deploya via GitHub Actions för att starta igen

---

## 🟢 STARTA API:et IGEN

### Om du pausade med Metod 1 (Max instances = 0):

**Steg:**

1. **Gå till Cloud Run service:**
   ```
   https://console.cloud.google.com/run/detail/us-central1/loneprocess-api?project=loneprocess-api-staging
   ```

2. **Klicka "EDIT & DEPLOY NEW REVISION"**

3. **Under "Revision scaling":**
   - Minimum number of instances: `0` (lämna som det är)
   - **Maximum number of instances: Ändra till `10`** ⬅️ AKTIVERAR!

4. **Klicka "DEPLOY"**

5. **Vänta ~30 sekunder**

**Resultat:**
- ✅ API:et är **live** igen
- ✅ URL fungerar: https://loneprocess-api-922770673146.us-central1.run.app
- ✅ Samma konfiguration som innan

---

### Om du deletade servicen (Metod 2):

**Steg:**

1. **Gå till GitHub repo:**
   ```
   https://github.com/carlgerhardsson/loneprocess-api
   ```

2. **Gör en push till `staging` branch** (eller re-run senaste workflow)

   ```bash
   # Lokalt:
   git checkout staging
   git commit --allow-empty -m "chore: Trigger redeploy"
   git push
   ```

   **ELLER** via GitHub Actions UI:
   - Gå till: https://github.com/carlgerhardsson/loneprocess-api/actions
   - Välj "Deploy to Cloud Run" workflow
   - Klicka "Re-run all jobs"

3. **Vänta ~5 minuter** för full deployment

**Resultat:**
- ✅ API:et är deployat på nytt
- ✅ Samma URL: https://loneprocess-api-922770673146.us-central1.run.app
- ✅ All konfiguration återställd

---

## 🔄 DISABLE AUTO-DEPLOY (Stoppa GitHub Actions)

**När du vill:** Förhindra nya deployments, men låt nuvarande servicen köra

**Steg:**

1. **Gå till GitHub Actions:**
   ```
   https://github.com/carlgerhardsson/loneprocess-api/actions
   ```

2. **Klicka på "Deploy to Cloud Run" workflow** (i vänstermenyn)

3. **Klicka "..." (tre prickar)** → **"Disable workflow"**

**Resultat:**
- ✅ Inga nya deployments vid push till staging
- ⚠️ Nuvarande service körs fortfarande (om redan deployad)
- ⚠️ Kostar pengar om servicen är aktiv

**För att aktivera igen:**
- Samma steg, men klicka **"Enable workflow"**

---

## 📊 KOSTNADSUPPSKATTNING

### När Pausad (Max instances = 0)
```
Cost: $0/månad
Reason: Inga containers körs
```

### När Aktiv med Rate Limiting
```
Max requests: 60 req/min = 2.6M req/månad
Cloud Run free tier: 2M req/månad gratis
Cost: $0/månad (inom free tier)
```

### Om Free Tier Överskrids
```
Over 2M requests:
- $0.40 per 1M requests
- $0.024 per vCPU-second
- $0.0025 per GiB-second memory

Budget alert: $5/månad (satt i Firebase Console)
```

---

## ⚠️ VIKTIGA PUNKTER

**1. Rate Limiting Skyddar Mot Oväntade Kostnader**
- Max 60 requests/min = 2.6M requests/månad
- Garanterar att vi stannar inom free tier
- Skyddar mot DDoS/missbruk

**2. Minimum Instances = 0 är Rätt för Staging**
- Inga "always-on" containers
- Startar bara vid requests
- Ingen kostnad när ingen använder

**3. Budget Alert = $5/månad**
- Email varning om kostnader överstiger $5
- Extra säkerhetsnät
- Kan ändras i Firebase Console

---

## 🎯 REKOMMENDATIONER

**För Staging/Test:**
- ✅ Pausa när du inte använder (Max instances = 0)
- ✅ Starta bara när du testar/utvecklar
- ✅ Behåll rate limiting (60 req/min)

**För Production (framtida):**
- Min instances: 1-2 (för snabbare response)
- Max instances: 50-100 (för skalning)
- Ta bort/höj rate limit
- Uppgradera till större instanser

---

## 📞 Support

**Problem med att pausa/starta?**
- Kontakt: carl.gerhardsson@cgi.com
- GitHub Issues: https://github.com/carlgerhardsson/loneprocess-api/issues
- Cloud Console Logs: https://console.cloud.google.com/run/detail/us-central1/loneprocess-api/logs?project=loneprocess-api-staging

---

**Senast uppdaterad:** 2026-03-12
**Status:** 🟢 Active deployment med pauserings-möjlighet
