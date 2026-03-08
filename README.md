# Löneprocess Digital Checklista API v3.0

**Komplett FastAPI backend för löneprocesshantering med LA-integration**

## 🚀 Vad är nytt i v3.0?

### ✨ Modulär Struktur
- Uppdelat i logiska moduler för bättre underhåll
- Lättare att hitta och uppdatera kod
- Production-ready arkitektur

### 🔴 Nya Funktioner (från v2.1)
- **FELLISTOR** - Hantera fel från löneberäkningar (Must-have!)
- **KÖRNINGSSTATUS** - Status för provlön och slutlön (Must-have!)

## 📁 Projektstruktur

```
loneprocess-api/
├── config.py              # Konfiguration
├── database.py            # Databas (SQLite)
├── models.py              # Pydantic modeller
├── main.py                # FastAPI app + alla endpoints
├── requirements.txt       # Dependencies
├── README.md              # Denna fil
└── .env.example          # Environment variabler exempel
```

## 🎯 Snabbstart

### 1. Installera dependencies

```bash
pip install -r requirements.txt
```

### 2. Starta servern

```bash
python main.py
```

### 3. Öppna Swagger UI

```
http://localhost:8000/docs
```

## 📚 API Endpoints

### Original Features
- `GET/POST/PUT/DELETE /api/v1/activities` - Aktivitetshantering
- `GET/POST/PUT /api/v1/loneperiods` - Löneperiodhantering  
- `GET /api/v1/loneperiods/{id}/progress` - Framdriftsspårning

### LA Integration
- `POST /api/v1/la/sync/employees` - Synka anställda från LA
- `GET /api/v1/la/employees` - Hämta synkade anställda
- `GET /api/v1/la/absences` - Hämta frånvaro
- `GET /api/v1/la/vacation-balances` - Semestersaldon

### v3.0 - Fellistor & Körningsstatus
- `GET /api/v1/la/fellistor/{period_id}` - Hämta fellista
- `GET /api/v1/la/fellistor/{period_id}/summary` - Sammanfattning
- `PATCH /api/v1/la/fellistor/{error_id}` - Markera behandlat
- `GET /api/v1/la/periods/{id}/korningsstatus` - Hämta körningsstatus
- `PATCH /api/v1/la/periods/{id}/korningsstatus` - Uppdatera status

## 🔧 Konfiguration

### Environment Variabler

```bash
# Database
DB_NAME=loneprocess.db

# LA Integration
LA_USE_MOCK=true
LA_API_URL=http://localhost:8000/api/la-mock/v1
LA_API_KEY=your-api-key

# CORS
CORS_ORIGINS=*
```

## 🧪 Testa API:et

### Via Swagger UI (Rekommenderat)
1. Öppna http://localhost:8000/docs
2. Klicka "Try it out" på valfri endpoint
3. Testa direkt i browsern

### Via cURL

```bash
# Hämta aktiviteter
curl http://localhost:8000/api/v1/activities

# Skapa löneperiod
curl -X POST http://localhost:8000/api/v1/loneperiods \
  -H "Content-Type: application/json" \
  -d '{"name":"April 2026","start_date":"2026-04-01","end_date":"2026-04-30"}'

# Hämta fellista
curl http://localhost:8000/api/v1/la/fellistor/1/summary
```

## 🗄️ Databas

API:et använder SQLite med följande tabeller:

### Original
- `activities` - Löneprocessaktiviteter
- `loneperiods` - Löneperioder
- `assignments` - Kopplingar mellan aktiviteter och perioder

### LA Integration
- `la_employees` - Anställda från LA
- `la_period_mappings` - Periodmappningar
- `la_absences` - Frånvaro
- `la_vacation_balances` - Semestersaldon
- `la_benefits` - Förmåner
- `la_tax_info` - Skatteinformation

### v3.0
- `la_calculation_errors` - Fellistor
- `la_sync_log` - Synkroniseringslogg

## 📖 Dokumentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## 🔐 Säkerhet

### Development
- CORS är öppet (`*`) för utveckling
- Ingen autentisering krävs

### Production (TODO)
- [ ] Lägg till JWT autentisering
- [ ] Begränsa CORS till specifika domains
- [ ] Lägg till rate limiting
- [ ] Använd PostgreSQL istället för SQLite
- [ ] Aktivera HTTPS

## 🚀 Deployment

### Development
```bash
python main.py
```

### Production (exempel med Gunicorn)
```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📝 Versionshistorik

### v3.0.0 (2026-03-04)
- ✨ Modulär struktur
- ✨ Fellistor (Must-have)
- ✨ Körningsstatus (Must-have)
- 🔧 Förbättrad dokumentation

### v2.1.0 (2026-02-18)
- ✨ LA Integration grundfunktioner
- ✨ Mock API för utveckling

### v1.0.0 (2026-01-30)
- ✨ Initial release
- ✨ Aktivitetshantering
- ✨ Löneperiodhantering

## 🤝 Bidra

Detta är ett internt projekt. Kontakta teamet för frågor.

## 📧 Support

- **Email:** support@loneprocess.se
- **Team:** Löneprocess Development Team

## 📄 License

Proprietary - Internal use only

---

**Made with ❤️ by Löneprocess Team**
