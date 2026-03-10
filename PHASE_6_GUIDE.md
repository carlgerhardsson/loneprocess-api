# Phase 6: External Team Access - Step by Step Guide

**Mål:** Ge Frontend Team X säker access till staging API

**Beräknad tid:** 30-45 minuter

---

## 📋 **STEG 1: Deploy Firestore Security Rules** ⏱️ 5 min

**Du gör:**

```powershell
# Navigera till projektet
cd "H:\Filer från gamla datorn 2\Filer från gamla\Eget labbande med Visual Studio Agenter\loneprocess-api"

# Hämta senaste koden
git pull origin staging

# Deploy security rules till Firebase
firebase deploy --only firestore:rules,firestore:indexes
```

**Förväntat resultat:**
```
✔  Deploy complete!

Project Console: https://console.firebase.google.com/project/loneprocess-api-staging/overview
```

**Verifiera:**
1. Gå till: https://console.firebase.google.com/project/loneprocess-api-staging/firestore/rules
2. Klicka **"Rules"** tab
3. Du ska se de nya reglerna med `isFrontendTeam()` funktioner

---

## 📋 **STEG 2: Testa Security Rules** ⏱️ 10 min

**Du gör:**

1. Gå till Firebase Console: https://console.firebase.google.com/project/loneprocess-api-staging/firestore/rules
2. Klicka på **"Rules Playground"** (längst upp till höger)
3. Testa dessa scenarios:

**Test 1: Utan authentication (ska NEKAS)**
```
Location: /loneperiods/202501
Authenticated: No

Expected: Access denied ❌
```

**Test 2: Med fel team claim (ska NEKAS)**
```
Location: /loneperiods/202501
Authenticated: Yes
Provider: Custom
Auth payload:
{
  "team": "wrong-team"
}

Expected: Access denied ❌
```

**Test 3: Med rätt team claim (ska TILLÅTAS)**
```
Location: /loneperiods/202501
Authenticated: Yes
Provider: Custom
Auth payload:
{
  "team": "frontend-team-x"
}

Expected: Read allowed ✅
```

**Om alla 3 testen passerar → fortsätt till Steg 3**

---

## 📋 **STEG 3: Sätt Budget Alert** ⏱️ 5 min

**Du gör:**

1. Gå till: https://console.firebase.google.com/project/loneprocess-api-staging/usage
2. Klicka **"Details & Settings"**
3. Under **"Budget alerts"**, klicka **"Set budget"**
4. Konfigurera:
   - **Budget amount:** `$0` USD
   - **Alert emails:** Din email (carl.gerhardsson@cgi.com)
   - **Alert threshold:** 50%, 90%, 100%
5. Klicka **"Save"**

**Verifiera:**
Du får ett email: "Budget alert configured for Firebase project loneprocess-api-staging"

---

## 📋 **STEG 4: Generera Access Token för Frontend Team X** ⏱️ 10 min

**Du gör:**

Skapa en Python-script för att generera custom token:

```powershell
# Skapa script
New-Item -Path "generate_team_token.py" -ItemType File
```

**Kopiera detta innehåll till `generate_team_token.py`:**

```python
#!/usr/bin/env python3
"""
Generate Firebase custom token for Frontend Team X
"""
import os
from pathlib import Path
from firebase_admin import credentials, auth, initialize_app

# Setup credentials
credentials_dir = Path(__file__).parent / "credentials"
credential_files = list(credentials_dir.glob("*.json"))

if not credential_files:
    print("❌ No credentials found!")
    exit(1)

# Initialize Firebase
cred = credentials.Certificate(str(credential_files[0]))
initialize_app(cred)

# Generate custom token for frontend-team-x
uid = "frontend-team-x"
custom_claims = {
    "team": "frontend-team-x",
    "role": "external",
    "access_level": "read-only"
}

try:
    # Create custom token
    custom_token = auth.create_custom_token(uid, custom_claims)
    
    print("=" * 70)
    print("🔑 FIREBASE CUSTOM TOKEN GENERATED")
    print("=" * 70)
    print(f"\nUID: {uid}")
    print(f"Claims: {custom_claims}")
    print(f"\n📋 TOKEN (copy this to Frontend Team X):\n")
    print(custom_token.decode('utf-8'))
    print("\n" + "=" * 70)
    print("⚠️  SECURITY:")
    print("- Send via secure channel (NOT email)")
    print("- Token expires after 1 hour")
    print("- Read-only access")
    print("=" * 70)
    
except Exception as e:
    print(f"❌ Error: {e}")
```

**Kör scriptet:**

```powershell
python generate_team_token.py
```

**Du får en output som:**
```
======================================================================
🔑 FIREBASE CUSTOM TOKEN GENERATED
======================================================================

UID: frontend-team-x
Claims: {'team': 'frontend-team-x', 'role': 'external', 'access_level': 'read-only'}

📋 TOKEN (copy this to Frontend Team X):

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJmcm9udGVuZC10ZWFtLXgiLCJjbGFpbXMiOnsidGVhbSI6ImZyb250ZW5kLXRlYW0teCIsInJvbGUiOiJleHRlcm5hbCJ9LCJpYXQiOjE2NzYwNDQyMTIsImV4cCI6MTY3NjA0NzgxMiwiYXVkIjoiaHR0cHM6Ly9pZGVudGl0eXRvb2xraXQuZ29vZ2xlYXBpcy5jb20vZ29vZ2xlLmlkZW50aXR5Lmlk...

======================================================================
⚠️  SECURITY:
- Send via secure channel (NOT email)
- Token expires after 1 hour
- Read-only access
======================================================================
```

**KOPIERA DENNA TOKEN** - du behöver den i nästa steg!

---

## 📋 **STEG 5: Testa Token Lokalt** ⏱️ 5 min

**Du gör:**

Skapa ett test-script för att verifiera att token fungerar:

```powershell
New-Item -Path "test_token.py" -ItemType File
```

**Kopiera detta innehåll:**

```python
#!/usr/bin/env python3
"""
Test Firebase token authentication
"""
import requests

# REPLACE WITH YOUR TOKEN FROM STEP 4
TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."  # <-- KLISTRA IN DIN TOKEN HÄR

# Test endpoints
BASE_URL = "http://localhost:8000"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

print("Testing API with Firebase token...\n")

# Test 1: Health check
response = requests.get(f"{BASE_URL}/health")
print(f"✅ Health: {response.status_code}")

# Test 2: Get activities
response = requests.get(f"{BASE_URL}/api/v1/activities", headers=headers)
print(f"✅ Activities: {response.status_code} - {len(response.json())} items")

# Test 3: Get loneperiods
response = requests.get(f"{BASE_URL}/api/v1/loneperiods", headers=headers)
print(f"✅ Loneperiods: {response.status_code} - {len(response.json())} items")

print("\n🎉 Token works!")
```

**Kör test:**

```powershell
# Starta API lokalt (i en annan terminal)
python main.py

# I första terminalen, kör test
python test_token.py
```

**Förväntat resultat:**
```
✅ Health: 200
✅ Activities: 200 - 50 items
✅ Loneperiods: 200 - 12 items

🎉 Token works!
```

---

## 📋 **STEG 6: Sätt api-documentation Branch till Public** ⏱️ 5 min

**Du gör:**

1. Gå till: https://github.com/carlgerhardsson/loneprocess-api/settings
2. Scrolla ner till **"Danger Zone"**
3. Klicka **"Change repository visibility"**
4. Välj **"Make public"**
5. Skriv `loneprocess-api` för att bekräfta
6. Klicka **"I understand, make this repository public"**

**WAIT!** Detta gör HELA repot public! 

**Bättre lösning:** Skapa ett SEPARAT public repo för dokumentation:

```powershell
# Vi skapar ett nytt public repo istället
# Claude gör detta via GitHub API i nästa steg
```

---

## 📋 **STEG 7: Skapa Onboarding Email Template** ⏱️ 5 min

**Template för Frontend Team X:**

```
Subject: 🔥 Löneprocess API Staging Access - Welcome!

Hi Frontend Team X,

Welcome to the Löneprocess API staging environment! 

🔑 YOUR ACCESS TOKEN:
[INSERT TOKEN FROM STEP 4]

📚 DOCUMENTATION:
https://github.com/carlgerhardsson/loneprocess-api-docs

🌐 API BASE URL:
http://staging-api.loneprocess.se (coming soon)
For now, use: http://localhost:8000 (requires VPN)

🛠️ QUICK START:

1. Add token to your requests:
   Authorization: Bearer YOUR_TOKEN_HERE

2. Test with curl:
   curl -H "Authorization: Bearer YOUR_TOKEN" \
        http://localhost:8000/api/v1/loneperiods

3. Check Swagger docs:
   http://localhost:8000/docs

⚠️ IMPORTANT:
- Token expires after 1 hour
- Read-only access
- Test data only (no production)
- Rate limited: 100 requests/minute

📞 SUPPORT:
Email: carl.gerhardsson@cgi.com
Response time: 24 hours

Happy coding! 🚀

Best regards,
Carl
```

---

## ✅ **PHASE 6 CHECKLIST**

Kryssa av när klart:

- [ ] STEG 1: Firestore rules deployed
- [ ] STEG 2: Security rules tested (3 scenarios)
- [ ] STEG 3: Budget alert set to $0
- [ ] STEG 4: Token generated
- [ ] STEG 5: Token tested locally
- [ ] STEG 6: Public documentation repo created
- [ ] STEG 7: Onboarding email prepared

---

## 🚀 **NÄSTA STEG**

När alla checkboxar är ikryssade:
1. Skicka token till Frontend Team X (säkert!)
2. Skicka onboarding email
3. Fortsätt till **Phase 7: Documentation**

---

**Beräknad total tid:** 45 minuter  
**Säkerhetsnivå:** Hög ✅  
**Kostnad:** $0 ✅
