# 💰 Kostnadskontroll - Pausa API:et

## ⚠️ VIKTIGT: Cloud Run Policy

**Google Cloud Run tillåter INTE Max instances = 0 längre.**
- Minimum: 1 instance
- Kostnad med 1 instance: ~$2-3/månad även när oanvänd

**Lösning för $0:** Delete servicen när du inte använder den.

---

## 🔴 PAUSA (Delete Service) = $0/månad

### Steg:

**1. Gå till Cloud Run:**
```
https://console.cloud.google.com/run?project=loneprocess-api-staging
```

**2. Markera checkbox** bredvid `loneprocess-api`

**3. Klicka "DELETE"** (papperskorgen)

**4. Bekräfta**

**Resultat:**
- ✅ **$0 kostnad**
- ❌ URL fungerar inte
- ✅ All config sparad i Git

---

## 🟢 STARTA IGEN (~5 minuter)

### Via GitHub (Rekommenderat):

**1. Push till staging branch:**
```bash
git checkout staging
git commit --allow-empty -m "chore: Redeploy"
git push
```

**2. ELLER re-run GitHub Actions:**
- Gå till: https://github.com/carlgerhardsson/loneprocess-api/actions
- Välj "Deploy to Cloud Run"
- Klicka "Re-run all jobs"

**3. Vänta ~5 minuter**

**Resultat:**
- ✅ API live igen
- ✅ Samma URL
- ✅ All config återställd

---

## 📊 KOSTNADER

### Deletad Service
```
Cost: $0/månad
```

### Aktiv med Rate Limit (Min: 0, Max: 10)
```
Max: 2.6M req/månad (60 req/min limit)
Free tier: 2M req/månad
Cost: $0/månad (inom free tier)
```

### Med Min instances = 1 (EJ REKOMMENDERAT)
```
1 instance × 0.25 vCPU × 128MB × 730 hr
Cost: ~$2-3/månad (även när oanvänd)
```

---

## 🎯 REKOMMENDATION

**För Staging/Test:**
1. ✅ **Delete servicen när du inte använder**
2. ✅ **Deploy via GitHub när du testar**
3. ✅ **Tar 5 min att starta igen**

**För Production:**
- Min instances: 1-2
- Max instances: 50-100
- Acceptera $2-3/månad för snabbare response

---

## 📞 Support

**Frågor?**
- carl.gerhardsson@cgi.com
- https://github.com/carlgerhardsson/loneprocess-api/issues
