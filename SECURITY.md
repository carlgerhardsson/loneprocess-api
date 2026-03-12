# 🔐 Säkerhetsguide - Skydda API:et

## ⚠️ NUVARANDE STATUS

**API:et är PUBLIKT TILLGÄNGLIGT:**
- URL: https://loneprocess-api-922770673146.us-central1.run.app
- Ingen autentisering krävs
- Vem som helst kan anropa endpoints

**SKYDD SOM FINNS:**
- ✅ Rate limiting: 60 requests/min per IP
- ✅ Budget alert: $5/månad
- ✅ Obskyr URL (svår att gissa)

**SKYDD SOM SAKNAS:**
- ❌ Ingen IP whitelist
- ❌ Ingen Firebase Auth enforcement
- ❌ Ingen API key requirement

---

## 🎯 RISKER

### Hög Risk: Data Läckning
- Vem som helst kan läsa Firestore data
- Lönedata, fellistor, anställda synliga
- **Mitigation:** Obskyr URL + testdata

### Medelhög Risk: Data Manipulation  
- Vem som helst kan ändra/ta bort data
- **Mitigation:** Testdata (kan re-seeda)

### Låg Risk: DoS Attack
- Spamming blockeras av rate limit
- **Mitigation:** 60 req/min max = $0-5/månad

---

## 🛡️ SÄKERHETSNIVÅER

### NIVÅ 1: IP Whitelist (Snabbaste)

**För:** Staging/test med kända användare

**Steg via Cloud Console:**

1. Gå till Cloud Run service:
   ```
   https://console.cloud.google.com/run/detail/us-central1/loneprocess-api?project=loneprocess-api-staging
   ```

2. Klicka "EDIT & DEPLOY NEW REVISION"

3. Gå till "Security" tab

4. Under "Ingress control":
   - Välj "Internal and Cloud Load Balancing"
   ELLER
   - Använd Cloud Armor för IP filtering

**Resultat:**
- ✅ Endast dina IP:er kan anropa
- ✅ Enkel att implementera
- ❌ Kräver uppdatering vid nya IPs

---

### NIVÅ 2: API Keys (Rekommenderat)

**För:** Kontrollerad åtkomst till externa teams

**Implementation i kod:**

```python
# I main.py
from fastapi import Header, HTTPException

VALID_API_KEYS = {
    "team-x-key-abc123": "Frontend Team X",
    "team-y-key-xyz789": "Mobile Team Y"
}

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return VALID_API_KEYS[x_api_key]

# Lägg till i endpoints:
@app.get("/api/v1/activities", dependencies=[Depends(verify_api_key)])
def get_activities():
    ...
```

**Resultat:**
- ✅ Kontrollerad åtkomst per team
- ✅ Kan revokera keys
- ✅ Spårbar användning

---

### NIVÅ 3: Firebase Auth (Production)

**För:** Full produktion med user management

**Implementation:**

```python
# I main.py
from firebase_admin import auth
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        return decoded_token
    except:
        raise HTTPException(status_code=401, detail="Invalid authentication")

# Lägg till i endpoints:
@app.get("/api/v1/activities", dependencies=[Depends(verify_token)])
def get_activities():
    ...
```

**Resultat:**
- ✅ Full user management
- ✅ Role-based access control
- ✅ Production-ready

---

### NIVÅ 4: Firestore Security Rules

**För:** Database-level säkerhet

**I Firebase Console:**

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Kräv autentisering för all access
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
    
    // Eller mer granulär:
    match /activities/{activityId} {
      allow read: if request.auth != null;
      allow write: if request.auth.token.admin == true;
    }
  }
}
```

**Resultat:**
- ✅ Skydd även om API bypassas
- ✅ Granulär kontroll per collection
- ✅ Defense in depth

---

## 📊 REKOMMENDATION FÖR STAGING

**Nivå 1 + Nivå 2 kombination:**

1. ✅ **Behåll rate limiting** (60 req/min)
2. ✅ **Lägg till API keys** för frontend teams
3. ✅ **Dela INTE URL:en publikt**
4. ⚠️ **Använd testdata** (ingen produktionsdata)

**Kostnad:** $2-3/månad + $0 för extra säkerhet

---

## 🚨 OM NÅGON HITTAR URL:EN

**Vad kan hända:**
- De ser testdata (ingen känslig data)
- De begränsas till 60 req/min
- Budget alert vid $5
- Du kan se alla requests i Cloud Logs

**Vad du gör:**
1. Kolla logs: https://console.cloud.google.com/run/detail/us-central1/loneprocess-api/logs?project=loneprocess-api-staging
2. Om missbruk: Deploy ny revision med API keys
3. Om mycket missbruk: Pausa/delete service

---

## 📞 AKUT RESPONS

**Om du ser misstänkt aktivitet:**

**1. Kolla logs omedelbart:**
```
https://console.cloud.google.com/run/detail/us-central1/loneprocess-api/logs?project=loneprocess-api-staging
```

**2. Pausa service (DELETE):**
```
https://console.cloud.google.com/run?project=loneprocess-api-staging
```

**3. Re-seed Firestore vid korrupt data:**
```bash
python seed_firestore.py
```

---

## ✅ NÄSTA STEG

**Vad vill du göra?**

1. ⭐ **Inget just nu** - Obskyr URL räcker för staging
2. 🔐 **Lägg till API keys** - För frontend teams
3. 🛡️ **Firebase Auth** - Full production security
4. 🌐 **IP Whitelist** - Endast dina IPs

Vad passar bäst för ditt användningsfall?
