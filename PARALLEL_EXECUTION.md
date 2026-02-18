# 🚀 Running API v1 and v2 in Parallel

Löneprocess API now supports running both v1 and v2 simultaneously on different ports!

## 📊 Quick Start

### Option 1: Python Script (Recommended)
```bash
python run_both_apis.py
```

This will:
- Start API v1 on **port 8000**
- Start API v2 on **port 8001**
- Display both Swagger UIs and health endpoints
- Monitor both processes

### Option 2: PowerShell Script
```powershell
.\run_both_versions.ps1
```

### Option 3: Manual - Run separately in different terminals

**Terminal 1 - API v1:**
```bash
cd loneprocess-api
python standalone_api.py
```

**Terminal 2 - API v2:**
```bash
cd loneprocess-api
python standalone_api_v2.py --port 8001
```

---

## 🌐 Access the APIs

### API v1 (Port 8000)
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### API v2 (Port 8001)
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **Health Check**: http://localhost:8001/health
- **OpenAPI JSON**: http://localhost:8001/openapi.json

---

## 📝 Key Differences

| Feature | v1 | v2 |
|---------|----|----|
| Port | 8000 | 8001 |
| Database | `loneprocess.db` | `loneprocess.db` (shared) |
| LA Integration | ❌ | ✅ |
| Mock LA API | ❌ | ✅ |
| Employee Sync | ❌ | ✅ |
| Absence Tracking | ❌ | ✅ |
| Vacation Balances | ❌ | ✅ |
| Benefits Management | ❌ | ✅ |
| Tax Information | ❌ | ✅ |
| Calculation Errors | ❌ | ✅ |

---

## 🔧 Configuration

### Environment Variables (Optional)

Create `.env` file in `loneprocess-api/` directory:

```env
# LA Integration Mode (v2 only)
LA_USE_MOCK=true                    # true = mock-data, false = real LA API
LA_API_URL=https://la-system.se/api
LA_API_KEY=your-api-key-here
```

Default is `LA_USE_MOCK=true` for testing.

---

## 🛑 Stopping the APIs

### If using `run_both_apis.py`:
Press **Ctrl+C** to stop both APIs gracefully.

### If running manually:
1. In each terminal, press **Ctrl+C**
2. Or kill the processes by PID:
   ```bash
   kill <v1_pid> <v2_pid>
   ```

---

## 📚 Testing with Swagger UI

1. Open http://localhost:8000/docs for v1
2. Open http://localhost:8001/docs for v2
3. Use "Try it out" button to test endpoints
4. Compare responses between versions

Example flow:
```
1. GET /health (check both are running)
2. GET /api/v1/loneperiods (retrieve periods)
3. POST /api/v1/activities (create activities)
4. GET /api/v1/activities/{id} (retrieve specific)
```

---

## 🐛 Troubleshooting

### Port already in use?
```bash
# Check what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :8001

# Kill the process (Windows)
taskkill /PID <PID> /F

# Kill the process (Mac/Linux)
kill -9 <PID>
```

### Database locked error?
- Both versions share the same `loneprocess.db`
- This is intentional for data consistency
- If you get locks, restart both APIs

### Import errors?
Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

---

## 📖 Documentation

- [API v1 README](README.md)
- [API v2 LA Integration](README_LA_INTEGRATION.md)
- [LA Field Mapping](LA_FIELD_MAPPING.md)
- [Quick Testing Guide](SNABBGUIDE_TESTNING.md)

---

## 🔄 Updating to Latest Version

```bash
# Pull latest changes
git pull origin feature/api-v2-la-integration

# Update dependencies
pip install -r requirements.txt --upgrade

# Run again
python run_both_apis.py
```

---

## 📞 Support

For issues, questions, or feature requests:
1. Check the documentation files
2. Review the Swagger UI documentation (http://localhost:PORT/docs)
3. Check the console output for error messages
4. Create an issue on GitHub

---

Happy testing! 🎉
