# Development Workflow - Ny Endpoint

**Komplett flöde från idé till production när vi utvecklar en ny endpoint**

---

## 🔄 **FULLSTÄNDIGT FLÖDE**

### **Scenario: Lägg till ny endpoint för semesterstatistik**

---

## 📋 **STEG 1: PLANERING (Du + Claude)**

**Du säger:**
> "Vi behöver en ny endpoint som visar semesterstatistik per anställd"

**Claude skapar:**
1. GitHub Issue med requirements
2. Design för endpoint (URL, request/response)
3. Database schema changes (om nödvändiga)

**Output:**
- Issue #5: "Add vacation statistics endpoint"
- API design dokumentation

---

## 💻 **STEG 2: LOKAL UTVECKLING (VS Code)**

### **2.1: Claude uppdaterar koden (via GitHub MCP)**

**Filer som ändras:**

#### A. `models.py` - Lägg till Pydantic model
```python
class VacationStatsResponse(BaseModel):
    employee_id: str
    total_days: int
    used_days: int
    remaining_days: int
```

#### B. `firebase_adapter.py` - Lägg till Firestore query
```python
def get_vacation_stats(self, employee_id: str):
    doc_ref = self.db.collection('vacation_stats').document(employee_id)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else None
```

#### C. `main.py` - Lägg till endpoint
```python
@app.get(\"/api/v1/employees/{employee_id}/vacation-stats\", 
         response_model=VacationStatsResponse)
def get_vacation_stats(employee_id: str):
    stats = db_adapter.get_vacation_stats(employee_id)
    if not stats:
        raise HTTPException(404, \"Stats not found\")
    return stats
```

**Claude pushar till staging branch:**
```
git push origin staging
```

---

### **2.2: Du testar lokalt**

**Terminal 1 (Du kör):**
```powershell
cd \"H:\\Filer från gamla datorn 2\\...\\loneprocess-api\"
git pull origin staging
python main.py
```

**Output:**
```
🔥 Löneprocess API v3.0 - STAGING
Swagger UI: http://localhost:8000/docs
```

**Terminal 2 (Du testar):**
```powershell
# Test new endpoint
curl http://localhost:8000/api/v1/employees/EMP001/vacation-stats
```

**Du kollar Swagger:**
- Gå till http://localhost:8000/docs
- Testa nya endpoint:en
- Verifiera response

---

## 🔥 **STEG 3: FIREBASE FIRESTORE (Data)**

### **3.1: Seed test data (om behövs)**

**Claude uppdaterar `seed_firestore.py`:**
```python
# Add vacation stats for test employees
for i in range(1, 101):
    vacation_stats = {
        \"employee_id\": f\"EMP{i:03d}\",
        \"total_days\": 25,
        \"used_days\": random.randint(0, 25),
        \"remaining_days\": 25 - random.randint(0, 25)
    }
    db.collection('vacation_stats').document(f\"EMP{i:03d}\").set(vacation_stats)
```

**Du kör:**
```powershell
python seed_firestore.py
```

**Verifiera i Firebase Console:**
1. Gå till: https://console.firebase.google.com/project/loneprocess-api-staging/firestore
2. Kolla collection: `vacation_stats`
3. Se att 100 anställda har stats

---

## 🧪 **STEG 4: TESTA MOT FIRESTORE**

**Du startar API:et igen:**
```powershell
python main.py
```

**Du testar:**
```bash
curl http://localhost:8000/api/v1/employees/EMP001/vacation-stats
```

**Förväntat svar:**
```json
{
  \"employee_id\": \"EMP001\",
  \"total_days\": 25,
  \"used_days\": 12,
  \"remaining_days\": 13
}
```

✅ **Fungerar lokalt!**

---

## 📚 **STEG 5: UPPDATERA DOKUMENTATION**

### **5.1: Intern dokumentation (private repo)**

**Claude uppdaterar:**
- `docs/PROJECT_HISTORY.md` - Lägg till ny endpoint
- `README.md` - Uppdatera endpoints lista

### **5.2: Extern dokumentation (public repo)**

**Claude uppdaterar i `loneprocess-api-docs`:**

#### A. `README.md`
```markdown
## API Endpoints

...
- `GET /api/v1/employees/{id}/vacation-stats` - Get vacation statistics
```

#### B. `INTEGRATION_GUIDE.md`
```javascript
// New example:
async getVacationStats(employeeId) {
  return this.request(`/api/v1/employees/${employeeId}/vacation-stats`);
}
```

#### C. `TEST_DATA.md`
```markdown
## Vacation Stats (100)
- All employees have vacation stats
- total_days: 25
- used_days: 0-25 (random)
```

#### D. `examples/javascript-example.js`
```javascript
// Example 6: Get vacation stats
const stats = await api.getVacationStats('EMP001');
console.log('Vacation stats:', stats);
```

---

## 🚀 **STEG 6: GITHUB ACTIONS (Automatisk - Partial Deploy)**

### **6.1: Vad deployas automatiskt NU:**

**När Claude pushar till staging:**
```bash
git push origin staging
```

**GitHub Actions kör automatiskt:**
```yaml
# .github/workflows/deploy-staging.yml
steps:
  - Install dependencies
  - Run tests (imports check)
  - Deploy to Firebase:
      ✅ firestore.rules (säkerhetsregler)
      ✅ firestore.indexes.json (database indexes)
      ❌ INTE main.py (API koden)
      ❌ INTE firebase_adapter.py
```

**Vad detta betyder:**
- ✅ Database rules uppdateras automatiskt
- ✅ Database indexes uppdateras automatiskt
- ❌ API koden finns BARA i GitHub (inte deployed)
- ❌ API:et körs FORTFARANDE bara lokalt på din dator

**Kolla workflow:**
https://github.com/carlgerhardsson/loneprocess-api/actions

---

### **6.2: Frontend Team X's situation NU:**

**Problem:**
```
Frontend Team X → ❌ KAN INTE nå din localhost:8000
```

**De måste:**
- Antingen vänta på Cloud Functions deployment
- Eller köra din kod lokalt själva (inte praktiskt)

---

## 🌐 **STEG 7: FRAMTIDA DEPLOYMENT (Cloud Functions)**

### **7.1: När vi är redo för production:**

**Vi uppdaterar GitHub Actions workflow:**
```yaml
# Lägg till detta i deploy-staging.yml
- name: Deploy API to Cloud Functions
  run: |
    firebase deploy --only functions
```

**Detta kommer deploya:**
```
✅ main.py → Cloud Functions
✅ firebase_adapter.py → Cloud Functions
✅ requirements-firebase.txt → Cloud Functions
```

**API blir tillgängligt på:**
```
https://loneprocess-api-staging.web.app/api/v1/employees/EMP001/vacation-stats
```

### **7.2: Frontend Team X kan då:**

```javascript
// Frontend Team X's kod (efter Cloud Functions deploy)
const api = new LoneprocessAPI(auth);

// Authenticate
await api.authenticate(customToken);

// Anropa LIVE API (inte localhost)
const stats = await api.getVacationStats('EMP001');
console.log('Employee has', stats.remaining_days, 'vacation days left');
```

**URL de använder:**
```
https://loneprocess-api-staging.web.app/api/v1/employees/EMP001/vacation-stats
```

✅ **Fungerar från DERAS datorer!**

---

## 📊 **SAMMANFATTNING AV FLÖDET**

### **NU (Current State):**

```
1. DU/CLAUDE: Planera ny endpoint
   ↓
2. CLAUDE: Skriver kod (models, adapter, main.py)
   ↓
3. CLAUDE: Push till GitHub staging
   ↓
4. GITHUB ACTIONS: 
   ✅ Deploy firestore.rules
   ✅ Deploy firestore.indexes
   ❌ INTE deploy main.py
   ↓
5. DU: git pull + python main.py (LOKALT)
   ↓
6. API körs på DIN dator (localhost:8000)
   ↓
7. Frontend Team X: ❌ Kan INTE nå API:et
```

### **FRAMTID (Med Cloud Functions):**

```
1. DU/CLAUDE: Planera ny endpoint
   ↓
2. CLAUDE: Skriver kod
   ↓
3. CLAUDE: Push till GitHub staging
   ↓
4. GITHUB ACTIONS:
   ✅ Deploy firestore.rules
   ✅ Deploy firestore.indexes
   ✅ Deploy main.py → Cloud Functions
   ↓
5. API körs på Google's servrar (ALLTID ONLINE)
   ↓
6. Frontend Team X: ✅ Kan använda API:et!
```

---

## 🔑 **NYCKELPUNKTER**

### **Var körs vad NU:**

| Vad | Var | Status |
|-----|-----|--------|
| **Din utveckling** | Lokal dator (`python main.py`) | ✅ Fungerar |
| **Database** | Firebase Firestore (Cloud) | ✅ Online |
| **Database Rules** | Firebase (auto-deployed) | ✅ Auto-update |
| **API Kod** | Bara i GitHub + din dator | ⚠️ INTE deployed |
| **API Production** | Cloud Functions | ❌ INTE konfigurerat än |

### **Vad Frontend Team X kan göra NU:**

| Vad | Möjligt? | Varför? |
|-----|----------|---------|
| Läsa dokumentation | ✅ Ja | Public repo |
| Få access token | ✅ Ja | Du genererar |
| Testa mot API | ❌ Nej | Körs på din localhost |
| Se test data i docs | ✅ Ja | Dokumenterat |
| Förbereda kod | ✅ Ja | Kan skriva integration |

---

## 💡 **EXEMPEL PÅ ETT KOMPLETT FLÖDE NU**

**Tid: ~30 minuter**

```
09:00 - Du: \"Vi behöver vacation stats endpoint\"
09:05 - Claude: Kod skriven, pushad till GitHub
09:06 - GitHub Actions: Deploy firestore.rules ✅
09:10 - Du: git pull, python main.py (LOKALT)
09:15 - Du: Testar i Swagger - fungerar! ✅
09:20 - Claude: Uppdaterar dokumentation
09:25 - Du: Verifierar i Firebase Console
09:30 - ✅ Endpoint fungerar LOKALT!
        ⚠️  Frontend Team X kan INTE använda än
        ⏳ Väntar på Cloud Functions deployment
```

---

## 🎯 **NEXT STEPS (För att Frontend Team X ska kunna använda):**

1. **Deploy till Cloud Functions** (vi gör detta senare)
2. Uppdatera GitHub Actions workflow
3. Testa deployed API
4. Ge URL till Frontend Team X

**För nu:** API:et fungerar lokalt för din utveckling och testning! ✅

---

**Questions?** Se [LESSONS_LEARNED.md](LESSONS_LEARNED.md) för tips!

**Skapad:** 2026-03-10  
**Uppdaterad:** 2026-03-11  
**Nästa review:** Vid Cloud Functions deployment
