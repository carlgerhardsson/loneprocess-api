# 🔐 HTTPS Setup Guide för Löneprocess API

**Till: Databas-teamet**  
**Från: Frontend-teamet**  
**Datum: 2026-01-30**

---

## 📋 Bakgrund

Frontend-appen körs i Claude artifacts (HTTPS) och kan därför inte göra HTTP-requests till `http://localhost:8000`. Vi behöver att backend körs med HTTPS.

---

## 🎯 Rekommenderad lösning: ngrok Tunnel

Detta är det enklaste sättet att få HTTPS utan att ändra någon kod.

### Steg 1: Installera ngrok

**Mac/Linux:**
```bash
brew install ngrok/ngrok/ngrok

# Eller ladda ner från:
# https://ngrok.com/download
```

**Windows:**
```bash
# Ladda ner från: https://ngrok.com/download
# Extrahera och lägg till i PATH
```

### Steg 2: Starta Backend (som vanligt)

```bash
cd loneprocess-api
python standalone_api.py
```

Backend körs nu på `http://localhost:8000`

### Steg 3: Starta ngrok Tunnel

Öppna en **NY terminal** (låt backend köra i den första):

```bash
ngrok http 8000
```

Du får en output typ:
```
ngrok                                                                    

Session Status                online
Account                       Your Name (Plan: Free)
Version                       3.0.0
Region                        Europe (eu)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

### Steg 4: Dela HTTPS-URL med Frontend-teamet

**VIKTIGT:** Kopiera HTTPS-URL:en (t.ex. `https://abc123.ngrok.io`) och skicka till Frontend-teamet.

De kommer uppdatera sin kod till:
```javascript
const API_BASE_URL = 'https://abc123.ngrok.io/api/v1';
```

### Steg 5: Testa att det fungerar

Öppna i webbläsare:
```
https://abc123.ngrok.io/docs
https://abc123.ngrok.io/api/v1/loneperiods
https://abc123.ngrok.io/health
```

Allt ska fungera via HTTPS nu! ✅

---

## 📝 Dagligt Arbetsflöde

Varje dag när ni utvecklar:

```bash
# Terminal 1: Starta backend
cd loneprocess-api
python standalone_api.py

# Terminal 2: Starta ngrok
ngrok http 8000

# Kopiera den nya ngrok-URL:en och skicka till Frontend
```

**OBS:** Gratis ngrok ger en ny URL varje gång. Meddela Frontend när URL:en ändras.

---

## 🔧 Alternativ Metod: Self-Signed SSL Certifikat

Om ni inte vill använda ngrok kan ni köra med lokalt SSL-certifikat:

### Steg 1: Generera Certifikat

```bash
cd loneprocess-api

# Skapa self-signed certifikat
openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365 \
  -subj "/CN=localhost"
```

Detta skapar:
- `cert.pem` (certifikat)
- `key.pem` (privat nyckel)

### Steg 2: Lägg till i .gitignore

```bash
echo "cert.pem" >> .gitignore
echo "key.pem" >> .gitignore
```

### Steg 3: Uppdatera standalone_api.py

Längst ner i filen, ändra:

```python
if __name__ == "__main__":
    import uvicorn
    import os
    
    # Kolla om SSL-certifikat finns
    cert_file = "cert.pem"
    key_file = "key.pem"
    
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print("🔐 Starting with HTTPS on port 8443...")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8443,
            ssl_keyfile=key_file,
            ssl_certfile=cert_file
        )
    else:
        print("🌐 Starting with HTTP on port 8000...")
        print("💡 To enable HTTPS, generate SSL certificates:")
        print("   openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365")
        uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Steg 4: Starta med HTTPS

```bash
python standalone_api.py
```

Backend körs nu på `https://localhost:8443`

### Steg 5: Acceptera Self-Signed Certifikat

Första gången du besöker `https://localhost:8443/docs`:
1. Webbläsaren varnar: "Your connection is not private"
2. Klicka "Advanced" → "Proceed to localhost (unsafe)"
3. Detta är OK för development

---

## 🚀 Production: Deploy till Molnet

För permanent HTTPS-URL, deploya till Railway eller Render:

### Railway (Rekommenderat)

1. Skapa konto på [railway.app](https://railway.app)
2. Installera Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```
3. Deploy:
   ```bash
   cd loneprocess-api
   railway login
   railway init
   railway up
   ```
4. Du får en permanent URL typ: `https://loneprocess-api.railway.app`

### Render (Alternativ)

1. Skapa konto på [render.com](https://render.com)
2. Välj "New Web Service"
3. Connecta GitHub repo
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python standalone_api.py`
5. Deploy!

---

## 📊 Jämförelse av Metoderna

| Metod | Pros | Cons | Rekommendation |
|-------|------|------|----------------|
| **ngrok** | ✅ Enklast<br>✅ Riktig HTTPS<br>✅ Ingen kod-ändring | ⚠️ URL ändras dagligen (gratis) | ⭐ **BÄST för development** |
| **Self-signed SSL** | ✅ Fungerar offline<br>✅ Stabil localhost URL | ⚠️ Certifikat-varningar<br>⚠️ Kan ha CORS-problem | OK för lokal testning |
| **Railway/Render** | ✅ Permanent URL<br>✅ Production-ready<br>✅ Automatisk HTTPS | ⚠️ Kräver deployment | ⭐ **BÄST för långsiktig** |

---

## 🔍 Felsökning

### Problem: ngrok säger "command not found"
**Lösning:** Installera ngrok (se Steg 1 ovan)

### Problem: Port 8000 redan används
**Lösning:**
```bash
# Hitta vad som använder porten
lsof -i :8000

# Döda processen
kill -9 [PID]
```

### Problem: CORS-fel även med HTTPS
**Lösning:** Kontrollera att CORS är konfigurerat i `standalone_api.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # För development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Problem: Frontend får fortfarande timeout
**Lösning:** 
1. Kontrollera att ngrok tunnel körs
2. Testa URL:en manuellt i webbläsare
3. Verifiera att Frontend använder rätt URL

---

## 📞 Kontakt

Om något inte fungerar, kontakta Frontend-teamet med:
- Vilken metod du använder
- Error-meddelanden
- URL:en du försöker använda

---

## ✅ Checklista för Setup

**Med ngrok (rekommenderat):**
- [ ] ngrok installerat
- [ ] Backend körs på port 8000
- [ ] ngrok tunnel startad
- [ ] HTTPS-URL kopierad och skickad till Frontend
- [ ] Testat att `/docs` fungerar via HTTPS

**Med Self-signed SSL:**
- [ ] Certifikat genererade (cert.pem, key.pem)
- [ ] Code uppdaterad i standalone_api.py
- [ ] Backend körs på port 8443
- [ ] Accepterat certifikat i webbläsare
- [ ] Meddelat Frontend om URL: `https://localhost:8443`

**Med Railway/Render:**
- [ ] Konto skapat
- [ ] Repo connectat
- [ ] Deployment lyckad
- [ ] URL testad
- [ ] URL skickad till Frontend

---

## 🎯 Nästa Steg

1. Välj metod (ngrok rekommenderas för development)
2. Följ stegen ovan
3. Skicka HTTPS-URL till Frontend-teamet
4. Frontend uppdaterar sin `API_BASE_URL`
5. Testa tillsammans!

---

**Lycka till! 🚀**

*Uppdaterad: 2026-01-30*  
*Version: 1.0*