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
@app.get("/api/v1/employees/{employee_id}/vacation-stats", 
         response_model=VacationStatsResponse)
def get_vacation_stats(employee_id: str):
    stats = db_adapter.get_vacation_stats(employee_id)
    if not stats:
        raise HTTPException(404, "Stats not found")
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
cd "H:\Filer från gamla datorn 2\...\loneprocess-api"
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
        "employee_id": f"EMP{i:03d}",
        "total_days": 25,
        "used_days": random.randint(0, 25),
        "remaining_days": 25 - random.randint(0, 25)
    }
    db.collection('vacation_stats').document(f"EMP{i:03d}").set(vacation_stats)
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
  "employee_id": "EMP001",
  "total_days": 25,
  "used_days": 12,
  "remaining_days": 13
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

## 🚀 **STEG 6: DEPLOY TILL STAGING**

### **6.1: GitHub Actions (automatisk)**

**När Claude pushar till staging:**
```bash
git push origin staging
```

**GitHub Actions kör automatiskt:**
```yaml
# .github/workflows/deploy-staging.yml
1. Install dependencies
2. Run tests
3. Deploy Firestore rules (om ändrade)
4. Deploy Firestore indexes (om ändrade)
```

**Kolla workflow:**
https://github.com/carlgerhardsson/loneprocess-api/actions

---

### **6.2: (Framtiden) Deploy till Cloud Functions**

**När vi är redo för production:**

```bash
# Deploy API till Firebase Cloud Functions
firebase deploy --only functions
```

**API blir tillgängligt på:**
```
https://loneprocess-api-staging.web.app/api/v1/employees/EMP001/vacation-stats
```

---

## 🌐 **STEG 7: FRONTEND TEAM X INTEGRERAR**

### **7.1: De ser uppdaterad dokumentation**

**Frontend Team X går till:**
https://github.com/carlgerhardsson/loneprocess-api-docs

**De ser:**
- Uppdaterad README med ny endpoint
- Code example i JavaScript
- Test data dokumentation

### **7.2: De implementerar**

```javascript
// Frontend Team X's kod
import { LoneprocessAPI } from './api-client';

const api = new LoneprocessAPI(auth);

// Authenticate (de har redan token)
await api.authenticate(customToken);

// Använda nya endpoint:en
const stats = await api.getVacationStats('EMP001');
console.log('Employee has', stats.remaining_days, 'vacation days left');
```

### **7.3: De testar mot staging**

```javascript
// Deras test
fetch('http://localhost:8000/api/v1/employees/EMP001/vacation-stats', {
  headers: {
    'Authorization': `Bearer ${idToken}`
  }
})
```

**Fungerar! ✅**

---

## 📊 **SAMMANFATTNING AV FLÖDET**

```
1. DU/CLAUDE: Planera ny endpoint (GitHub Issue)
   ↓
2. CLAUDE: Uppdatera kod (models, adapter, main.py)
   ↓
3. CLAUDE: Push till staging branch
   ↓
4. DU: git pull + python main.py (lokalt)
   ↓
5. DU: Testa i Swagger (http://localhost:8000/docs)
   ↓
6. CLAUDE: Seed test data (seed_firestore.py)
   ↓
7. DU: Verifiera i Firebase Console
   ↓
8. DU: Testa mot Firestore lokalt
   ↓
9. CLAUDE: Uppdatera dokumentation (båda repos)
   ↓
10. GITHUB ACTIONS: Auto-deploy Firestore rules
   ↓
11. (FRAMTID) FIREBASE: Deploy till Cloud Functions
   ↓
12. FRONTEND TEAM X: Läser docs, implementerar, testar
```

---

## 🔑 **NYCKELPUNKTER**

### **Var körs vad:**

| Vad | Var | När |
|-----|-----|-----|
| **Utveckling** | Din lokala dator | `python main.py` |
| **Database** | Firebase Cloud | Alltid online |
| **CI/CD** | GitHub Actions | Vid push till staging |
| **Production (framtid)** | Cloud Functions | När vi deployer |

### **Vem gör vad:**

| Vem | Gör vad |
|-----|---------|
| **DU** | Testar lokalt, verifierar, ger feedback |
| **CLAUDE** | Skriver kod, pushar till GitHub, uppdaterar docs |
| **GITHUB ACTIONS** | Kör tests, deployer Firestore rules |
| **FIREBASE** | Lagrar data, (framtid: kör API) |
| **FRONTEND TEAM X** | Läser docs, implementerar, testar mot API |

---

## 💡 **EXEMPEL PÅ ETT KOMPLETT FLÖDE**

**Tid: ~30 minuter**

```
09:00 - Du: "Vi behöver vacation stats endpoint"
09:05 - Claude: Issue #5 skapad, kod skriven, pushad
09:10 - Du: git pull, python main.py
09:15 - Du: Testar i Swagger - fungerar!
09:20 - Claude: Seed data, uppdaterar docs
09:25 - Du: Verifierar i Firebase Console
09:30 - ✅ KLART! Frontend Team X kan använda!
```

---

**Questions?** Se [LESSONS_LEARNED.md](LESSONS_LEARNED.md) för tips!

**Skapad:** 2026-03-10  
**Uppdaterad:** 2026-03-10  
**Nästa review:** Vid behov
