# 🚀 Löneprocess Digital Checklista API

En komplett REST API för hantering av löneprocessaktiviteter och löneperioder, byggd med FastAPI och SQLite.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

## 📋 Innehåll

- [Snabbstart](#-snabbstart)
- [Features](#-features)
- [Dokumentation](#-dokumentation)
- [Installation](#-installation)
- [API Endpoints](#-api-endpoints)
- [För Frontend-teamet](#-för-frontend-teamet)
- [Databas](#-databas)
- [Utveckling](#-utveckling)

## ⚡ Snabbstart

```bash
# 1. Klona repo
git clone https://github.com/[ditt-username]/loneprocess-api.git
cd loneprocess-api

# 2. Installera dependencies
pip install -r requirements.txt

# 3. Starta servern
python standalone_api.py
```

**Öppna Swagger UI:** http://localhost:8000/docs 🎉

## ✨ Features

- ✅ **FastAPI** - Modern, snabb Python web framework
- ✅ **SQLite** - Lokal databas (ingen setup behövs!)
- ✅ **Swagger UI** - Interaktiv API dokumentation
- ✅ **OpenAPI 3.1.0** - Automatiskt genererad spec
- ✅ **CORS** - Aktiverad för frontend integration
- ✅ **Pydantic** - Data validering och serialisering
- ✅ **Sample Data** - Färdig testdata inkluderad

## 📚 Dokumentation

När servern körs:

- **Swagger UI (Interaktiv):** http://localhost:8000/docs
- **ReDoc (Läsbar):** http://localhost:8000/redoc  
- **OpenAPI JSON:** http://localhost:8000/openapi.json

Offline dokumentation:
- [API Examples](docs/API_EXAMPLES.md) - Request/response exempel
- [Error Codes](docs/ERROR_CODES.md) - Felhantering
- [Frontend Integration](docs/FRONTEND_INTEGRATION.md) - Guide för frontend

## 🔧 Installation

### Krav

- Python 3.8 eller nyare
- pip

### Steg-för-steg

#### 1. Klona repository

```bash
git clone https://github.com/[ditt-username]/loneprocess-api.git
cd loneprocess-api
```

#### 2. (Valfritt) Skapa virtual environment

```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Installera dependencies

```bash
pip install -r requirements.txt
```

#### 4. Starta servern

```bash
python standalone_api.py
```

Servern startar på http://localhost:8000

## 📡 API Endpoints

### Activities (Aktiviteter)

| Method | Endpoint | Beskrivning |
|--------|----------|-------------|
| GET | `/api/v1/activities` | Hämta alla aktiviteter (med filtrering) |
| GET | `/api/v1/activities/{id}` | Hämta specifik aktivitet |
| POST | `/api/v1/activities` | Skapa ny aktivitet |
| PUT | `/api/v1/activities/{id}` | Uppdatera aktivitet |
| DELETE | `/api/v1/activities/{id}` | Ta bort aktivitet |

### Loneperiods (Löneperioder)

| Method | Endpoint | Beskrivning |
|--------|----------|-------------|
| GET | `/api/v1/loneperiods` | Hämta alla löneperioder |
| GET | `/api/v1/loneperiods/{id}` | Hämta specifik löneperiod |
| POST | `/api/v1/loneperiods` | Skapa ny löneperiod |
| PUT | `/api/v1/loneperiods/{id}` | Uppdatera löneperiod |
| GET | `/api/v1/loneperiods/{id}/progress` | Hämta framdrift |
| POST | `/api/v1/loneperiods/{id}/activities` | Lägg till aktiviteter |

### Health

| Method | Endpoint | Beskrivning |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/` | API information |

## 🎯 För Frontend-teamet

### Quick Start

```javascript
// Base URL
const API_URL = 'http://localhost:8000/api/v1';

// Hämta aktiviteter
const response = await fetch(`${API_URL}/activities`);
const activities = await response.json();

// Skapa aktivitet
const newActivity = await fetch(`${API_URL}/activities`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    process_nr: '10.9',
    out_input: 'Test aktivitet',
    roll: 'Lönespecialist'
  })
});
```

### TypeScript Types

Se [Frontend Integration Guide](docs/FRONTEND_INTEGRATION.md) för kompletta TypeScript definitions.

### Testing

1. Starta backend: `python standalone_api.py`
2. Öppna `docs/api_test.html` i browser för interaktiv testning

## 🗄️ Databas

### Schema

**3 Tabeller:**
- `activities` - Löneprocessaktiviteter
- `loneperiods` - Löneperioder  
- `assignments` - Koppling mellan löneperioder och aktiviteter

### Sample Data

Vid första start skapas automatiskt:
- **5 aktiviteter** (ID 1-5)
- **3 löneperioder** (Januari-Mars 2026)
- **4 assignments** för testning av progress tracking

### Databashantering

Databasen sparas som `loneprocess.db` i projektets rot.

**Visa data:**
```bash
sqlite3 loneprocess.db "SELECT * FROM activities;"
```

**Återställ databas:**
```bash
rm loneprocess.db
python standalone_api.py  # Skapar ny med sample data
```

## 💻 Utveckling

### Projektstruktur

```
loneprocess-api/
├── standalone_api.py          # Huvudapplikation
├── requirements.txt           # Python dependencies
├── loneprocess.db            # SQLite databas (skapas automatiskt)
├── README.md                 # Denna fil
├── docs/                     # Dokumentation
│   ├── API_EXAMPLES.md
│   ├── ERROR_CODES.md
│   ├── FRONTEND_INTEGRATION.md
│   └── api_test.html
└── .gitignore
```

### Köra i development mode

```bash
# Med auto-reload
uvicorn standalone_api:app --reload

# På annan port
uvicorn standalone_api:app --port 8001

# Tillgänglig från andra datorer
uvicorn standalone_api:app --host 0.0.0.0
```

### Testning

```bash
# Enkel test
curl http://localhost:8000/health

# Testa alla endpoints
open http://localhost:8000/docs
```

## 🔐 Säkerhet

**OBS:** Detta är en development/demo version. För production:

- [ ] Lägg till authentication (JWT)
- [ ] Implementera rate limiting
- [ ] Använd PostgreSQL istället för SQLite
- [ ] Sätt upp HTTPS
- [ ] Validera och sanitera all input
- [ ] Lägg till logging
- [ ] Sätt upp monitoring

## 📝 Licens

Proprietary - Endast för internt bruk.

## 👥 Team

**Backend Team:**
- Database Architect
- API Developer  
- Documentation Specialist
- Testing & QA

**Support:** support@loneprocess.se

## 🙏 Tack

Utvecklat med:
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLite](https://www.sqlite.org/)

---

**Senast uppdaterad:** 2026-01-30  
**Version:** 1.0.0
