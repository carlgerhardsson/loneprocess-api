"""
Configuration settings for Löneprocess API v3.0
"""
import os
from typing import Literal

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DB_NAME = os.getenv("DB_NAME", "loneprocess.db")

# ============================================================================
# LA INTEGRATION CONFIGURATION
# ============================================================================

LA_USE_MOCK = os.getenv("LA_USE_MOCK", "true").lower() == "true"
LA_API_URL = os.getenv("LA_API_URL", "http://localhost:8000/api/la-mock/v1")
LA_API_KEY = os.getenv("LA_API_KEY", "mock-api-key")

# ============================================================================
# API CONFIGURATION
# ============================================================================

API_TITLE = "Löneprocess Digital Checklista API v3.0"
API_VERSION = "3.0.0"
API_DESCRIPTION = """
# Löneprocess Digital Checklista API v3.0

Komplett API för löneprocesshantering med integration mot LA-systemet.

## 🎯 Funktioner

### Original Features
* **Aktivitetshantering** - CRUD operations för löneprocessaktiviteter
* **Löneperiodhantering** - Hantera löneperioder och deras status
* **Framdriftsspårning** - Mät completion percentage för löneperioder
* **Assignments** - Koppla aktiviteter till löneperioder

### LA Integration Features
* **LA Mock API** - Simulerar LA-systemets endpoints för utveckling
* **Employee Sync** - Hämta och synka anställda från LA
* **Period Mapping** - Koppla era perioder till LA:s löneperioder
* **Absence Tracking** - Frånvaro och tidsrapportering från LA
* **Vacation Balances** - Semestersaldon och intjänande
* **Benefits** - Förmånshantering (bil, bostad, etc)
* **Tax Info** - Skatter och avdrag
* **Sync Logging** - Spåra alla synkningar

### NYA v3.0 - KRITISKA FUNKTIONER
* **✨ FELLISTOR** - Hantera fel från löneberäkningar (Must-have!)
* **✨ KÖRNINGSSTATUS** - Status för provlön och slutlön (Must-have!)

## 📚 Användning

**Development Mode (Mock):** Sätt `LA_USE_MOCK=true`  
**Production Mode:** Sätt `LA_USE_MOCK=false` och konfigurera `LA_API_URL` och `LA_API_KEY`

## 🏗️ Arkitektur

Version 3.0 använder modulär struktur för bättre underhåll och skalbarhet.
"""

# ============================================================================
# CORS CONFIGURATION
# ============================================================================

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]
