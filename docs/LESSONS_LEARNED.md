# Lessons Learned

**Best practices och lärdomar från Firebase staging implementation**

---

## 🐛 Common Pitfalls & Solutions

### **1. Firebase Admin SDK är Synchronous**

**Problem:**  
Använde `async/await` i FastAPI endpoints med Firebase Admin SDK.

**Error:**
```python
RuntimeWarning: coroutine 'get_activities' was never awaited
```

**Solution:**
```python
# WRONG:
@app.get("/api/v1/activities")
async def get_activities():
    activities = await db_adapter.get_activities()  # Firebase is sync!
    return activities

# CORRECT:
@app.get("/api/v1/activities")
def get_activities():  # No async!
    activities = db_adapter.get_activities()  # No await!
    return activities
```

**Lesson:** Firebase Admin SDK är 100% synchronous. Använd INTE `async`/`await`.

---

### **2. Firestore Document IDs är Strings**

**Problem:**  
Pydantic models hade `id: int`, men Firestore IDs är strings.

**Error:**
```
ValidationError: id - value is not a valid integer
```

**Solution:**
```python
# WRONG:
class ActivityResponse(BaseModel):
    id: int  # Firestore IDs are strings!

# CORRECT:
class ActivityResponse(BaseModel):
    id: str  # Firestore document IDs are always strings
```

**Lesson:** Alla Firestore document IDs är strings, även om de ser ut som integers.

---

### **3. Firestore Timestamps är Speciella**

**Problem:**  
`created_at` och `updated_at` fields kunde inte valideras av Pydantic.

**Error:**
```
ValidationError: created_at - value is not a valid datetime
```

**Solution:**
```python
from typing import Any

# WRONG:
class BaseModel(BaseModel):
    created_at: datetime

# CORRECT:
class BaseModel(BaseModel):
    created_at: Any  # Firestore DatetimeWithNanoseconds
```

**Lesson:** Firestore använder `DatetimeWithNanoseconds`, inte Python `datetime`. Använd `Any`.

---

### **4. Firestore Security Rules Syntax**

**Problem:**  
Använde `timestamp` som variabelnamn i Firestore rules.

**Error:**
```
[E] timestamp is a package and cannot be used as variable name
```

**Solution:**
```javascript
// WRONG:
function notTooManyRequests() {
  return request.time > timestamp.date(2024, 1, 1);
}

// CORRECT:
function isValidRequest() {
  return request.time > timestamp.date(2024, 1, 1);  // timestamp är en funktion
}
```

**Lesson:** `timestamp` är reserverat ord i Firestore rules. Använd andra namn.

---

### **5. Git Merge Conflicts med .gitignore**

**Problem:**  
Lokala ändringar i `.gitignore` krockade med remote vid `git pull`.

**Error:**
```
error: Your local changes to the following files would be overwritten by merge:
        .gitignore
```

**Solution:**
```bash
# Option 1: Spara lokala ändringar
git stash
git pull origin staging
git stash pop

# Option 2: Kasta bort lokala ändringar
git checkout -- .gitignore
git pull origin staging
```

**Lesson:** Använd `git stash` för att temporärt spara lokala ändringar.

---

### **6. Credentials i Git**

**Problem:**  
Risk att committa Firebase service account keys.

**Prevention:**
```gitignore
# .gitignore - KRITISKT!
credentials/
*.json
!firebase.json
!firestore.indexes.json
!package.json
```

**Lesson:**  
1. Lägg till `credentials/` i `.gitignore` INNAN du laddar ner service account key
2. Dubbelkolla med `git status` innan varje commit
3. Använd `git ls-files credentials/` för att verifiera (ska vara tomt)

---

### **7. Firestore Data Types Mapping**

**Problem:**  
SQL data types mappade inte direkt till Firestore.

**Mapping Table:**

| SQL Type | Firestore Type | Pydantic Type |
|----------|----------------|---------------|
| INTEGER (id) | string (document ID) | str |
| VARCHAR | string | str |
| DATE | string (ISO format) | str |
| DATETIME | timestamp | Any |
| ENUM | string | str |
| BOOLEAN | boolean | bool |

**Lesson:** Alltid konvertera dates till ISO strings innan Firestore write.

---

## 🚀 Best Practices

### **Firebase:**

1. **Auto-detect credentials:**
```python
from pathlib import Path

credentials_dir = Path(__file__).parent / "credentials"
credential_files = list(credentials_dir.glob("*.json"))

if credential_files:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(credential_files[0].absolute())
```

2. **Handle Firebase initialization:**
```python
try:
    initialize_app(credentials.Certificate(credentials_path))
except ValueError:
    pass  # Already initialized
```

3. **Use absolute paths:**
```python
# WRONG:
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials/key.json'

# CORRECT:
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(Path('credentials/key.json').absolute())
```

### **Security:**

1. **Sätt budget alerts DIREKT:**
   - Firebase Console → Usage → Set budget: $0
   - Email alerts: 50%, 90%, 100%

2. **Testa Firestore rules i Console:**
   - Rules Playground → Test alla scenarios
   - Test INNAN deployment

3. **Separera public/private repos:**
   - Private: Källkod, credentials, intern docs
   - Public: API docs, examples, onboarding

### **Documentation:**

1. **Dokumentera medan du kodar:**
   - Skriv docs UNDER development, inte efter
   - Update docs varje gång API ändras

2. **Inkludera code examples:**
   - JavaScript (vanilla)
   - TypeScript (med types)
   - cURL (för testing)

3. **Onboarding checklist:**
   - Token generation
   - Email template
   - Security reminders

### **Testing:**

1. **Seed realistic data:**
   - Använd Faker för svenska namn
   - Realistic volumes (100 employees, not 5)
   - Cover all edge cases

2. **Test lokalt först:**
   - Kör `python main.py`
   - Testa alla endpoints i Swagger
   - Verifiera data i Firebase Console

---

## 📊 Performance Tips

### **Firestore Queries:**

1. **Använd indexes:**
```json
// firestore.indexes.json
{
  "indexes": [
    {
      "collectionGroup": "fellistor",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "loneperiod_id", "order": "ASCENDING" },
        { "fieldPath": "severity", "order": "ASCENDING" }
      ]
    }
  ]
}
```

2. **Limit queries:**
```python
# WRONG:
all_docs = db.collection('employees').get()

# CORRECT:
limited_docs = db.collection('employees').limit(100).get()
```

3. **Cache results:**
```python
# Simple in-memory cache
from functools import lru_cache

@lru_cache(maxsize=128)
def get_loneperiods():
    return db_adapter.get_loneperiods()
```

---

## ⚠️ What NOT to Do

### **❌ NEVER:**

1. Commit credentials to Git
2. Use production data in staging
3. Hardcode API keys in code
4. Skip .gitignore setup
5. Use `async/await` with Firebase Admin SDK
6. Assume Firestore IDs are integers
7. Deploy without testing locally first
8. Share tokens between teams
9. Ignore budget alerts
10. Skip documentation

### **✅ ALWAYS:**

1. Use environment variables for secrets
2. Test Firestore rules before deploy
3. Set budget alerts to $0
4. Document as you code
5. Use type hints (Pydantic)
6. Version control everything (except secrets)
7. Test with realistic data
8. Review security checklist before external access
9. Monitor usage in Firebase Console
10. Keep public/private repos separated

---

## 📚 Resources

### **Official Docs:**
- Firebase Admin SDK: https://firebase.google.com/docs/admin/setup
- Firestore Security Rules: https://firebase.google.com/docs/firestore/security/get-started
- FastAPI: https://fastapi.tiangolo.com/

### **Internal Docs:**
- SECURITY.md - Security policy
- PHASE_6_GUIDE.md - External access guide
- PROJECT_HISTORY.md - Complete project timeline

### **Public Docs:**
- https://github.com/carlgerhardsson/loneprocess-api-docs

---

**Last Updated:** 2026-03-10  
**Maintainer:** Carl Gerhardsson  
**Review:** Quarterly
