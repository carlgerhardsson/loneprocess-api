# Test Data Documentation

All data is **fake test data** - no production or sensitive information.

---

## 📊 Overview

| Collection | Count | Description |
|------------|-------|-------------|
| Employees | 100 | Swedish names, org codes |
| Löneperiods | 12 | Jan-Dec 2025 |
| Activities | 50 | Process activities |
| Fellistor | 120 | Error records |
| Assignments | 240 | Activity-period links |

---

## 👥 Employees (100)

### Sample:
```json
{
  "id": "EMP001",
  "namn": "Anna Andersson",
  "org_kod": "1001",
  "org_namn": "Ekonomi",
  "status": "active"
}
```

### Org Codes:
- `1001` - Ekonomi
- `1002` - HR
- `1003` - IT
- `1004` - Försäljning
- `1005` - Produktion

---

## 📅 Löneperiods (12)

### Sample:
```json
{
  "id": "202501",
  "period_namn": "2025-01",
  "start_date": "2025-01-01",
  "end_date": "2025-01-31",
  "status": "completed",
  "fas": "Avslut"
}
```

### Period IDs:
`202501` through `202512`

### Fas Values:
- `Förberedelse` - Preparation
- `Körning` - Running
- `Avstämning` - Reconciliation
- `Avslut` - Closing

---

## ✅ Activities (50)

### Sample:
```json
{
  "id": "ACT001",
  "namn": "Kontrollera semesterdagar",
  "process": "forberedelse",
  "ansvarig_roll": "Löneadministratör"
}
```

### Process Types:
- `forberedelse`
- `korning`
- `avstamning`
- `avslut`

---

## ❌ Fellistor (120)

### Sample:
```json
{
  "id": "ERR001",
  "loneperiod_id": "202501",
  "error_code": "E301",
  "severity": "error",
  "status": "unresolved"
}
```

### Severity:
- `error` - Critical
- `warning` - Review needed
- `info` - Informational

### Error Codes:
- `E3xx` - Errors
- `W1xx` - Warnings
- `I2xx` - Info

---

## 🔍 Usage Examples

```javascript
// Get all employees
GET /api/v1/la/employees?limit=100

// Get January period
GET /api/v1/loneperiods/202501

// Get errors for period
GET /api/v1/la/fellistor/202501?severity=error

// Filter by org
GET /api/v1/la/employees?org_kod=1001
```

---

## ⚠️ Important

- ✅ No PII (personally identifiable information)
- ✅ Fake Swedish names
- ✅ Test IDs only
- ✅ Consistent across requests
- ❌ Cannot modify via API (read-only)

---

**Questions?** Contact: carl.gerhardsson@cgi.com
