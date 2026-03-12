#!/usr/bin/env python3
"""
Löneprocess Digital Checklista API v3.0 - Firebase Staging
Main application file with Firestore backend + API Key Authentication
"""
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional, List

# Import Firebase adapter and models
# NOTE: config.py handles Firebase initialization - do not initialize again!
from firebase_adapter import FirestoreAdapter
from models import *
from rate_limiter import RateLimiter
from auth_middleware import api_key_auth

# ============================================================================
# CONFIG
# ============================================================================

API_TITLE = "Löneprocess Digital Checklista API"
API_VERSION = "3.0.1-staging"
API_DESCRIPTION = """
Löneprocess Digital Checklista API - Firebase Staging Environment

**Staging miljö för frontend-testning**

- Firestore Database (test data)
- **API Key Authentication Required** 🔐
- Rate Limited: 60 requests/minute
- Secure HTTPS only

**Authentication:**
All API endpoints require `X-API-Key` header.
Contact API administrator for access keys.
"""

CORS_ORIGINS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# ============================================================================
# FASTAPI APP SETUP
# ============================================================================

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# Rate Limiting Middleware - 60 requests per minute
app.add_middleware(RateLimiter, requests_per_minute=60)

# Initialize Firestore adapter
db_adapter = FirestoreAdapter()


# ============================================================================
# HEALTH ENDPOINTS (NO AUTH REQUIRED)
# ============================================================================

@app.get("/", tags=["Health"])
def root():
    """Root endpoint - No authentication required"""
    return {
        "message": "Löneprocess Digital Checklista API v3.0 - Staging",
        "version": API_VERSION,
        "environment": "staging",
        "database": "Firestore",
        "authentication": "API Key Required (X-API-Key header)",
        "rate_limit": "60 requests/minute",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint - No authentication required"""
    return {
        "status": "healthy",
        "version": API_VERSION,
        "environment": "staging",
        "database": "Firestore",
        "authentication": "API Key Required",
        "rate_limit": "60 requests/minute",
        "service": "Löneprocess API v3.0"
    }


# ============================================================================
# ACTIVITIES ENDPOINTS (AUTH REQUIRED)
# ============================================================================

@app.get("/api/v1/activities", response_model=List[ActivityResponse], 
         dependencies=[Depends(api_key_auth)], tags=["Activities"])
def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    process: Optional[str] = None,
    role: Optional[str] = None,
    status: Optional[str] = None
):
    """Hämta aktiviteter med filtrering - Requires API Key"""
    try:
        activities = db_adapter.get_activities(
            skip=skip,
            limit=limit,
            process=process,
            role=role,
            status=status
        )
        return activities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fel vid hämtning: {str(e)}")


@app.get("/api/v1/activities/{activity_id}", response_model=ActivityResponse,
         dependencies=[Depends(api_key_auth)], tags=["Activities"])
def get_activity(activity_id: int):
    """Hämta specifik aktivitet - Requires API Key"""
    activity = db_adapter.get_activity(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail=f"Aktivitet {activity_id} hittades inte")
    return activity


@app.post("/api/v1/activities", response_model=ActivityResponse, status_code=201,
          dependencies=[Depends(api_key_auth)], tags=["Activities"])
def create_activity(activity: ActivityCreate):
    """Skapa ny aktivitet - Requires API Key"""
    try:
        created = db_adapter.create_activity(activity.model_dump())
        return created
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Kunde inte skapa aktivitet: {str(e)}")


@app.put("/api/v1/activities/{activity_id}", response_model=ActivityResponse,
         dependencies=[Depends(api_key_auth)], tags=["Activities"])
def update_activity(activity_id: int, activity: ActivityUpdate):
    """Uppdatera aktivitet - Requires API Key"""
    updated = db_adapter.update_activity(activity_id, activity.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail=f"Aktivitet {activity_id} hittades inte")
    return updated


@app.delete("/api/v1/activities/{activity_id}", status_code=204,
            dependencies=[Depends(api_key_auth)], tags=["Activities"])
def delete_activity(activity_id: int):
    """Ta bort aktivitet - Requires API Key"""
    deleted = db_adapter.delete_activity(activity_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Aktivitet {activity_id} hittades inte")


# ============================================================================
# LONEPERIODS ENDPOINTS (AUTH REQUIRED)
# ============================================================================

@app.get("/api/v1/loneperiods", response_model=List[LoneperiodResponse],
         dependencies=[Depends(api_key_auth)], tags=["Loneperiods"])
def get_loneperiods(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    year: Optional[int] = None
):
    """Hämta löneperioder - Requires API Key"""
    try:
        periods = db_adapter.get_loneperiods(
            skip=skip,
            limit=limit,
            status=status,
            year=year
        )
        return periods
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fel vid hämtning: {str(e)}")


@app.get("/api/v1/loneperiods/{loneperiod_id}", response_model=LoneperiodResponse,
         dependencies=[Depends(api_key_auth)], tags=["Loneperiods"])
def get_loneperiod(loneperiod_id: int):
    """Hämta specifik löneperiod - Requires API Key"""
    period = db_adapter.get_loneperiod(loneperiod_id)
    if not period:
        raise HTTPException(status_code=404, detail=f"Löneperiod {loneperiod_id} hittades inte")
    return period


@app.post("/api/v1/loneperiods", response_model=LoneperiodResponse, status_code=201,
          dependencies=[Depends(api_key_auth)], tags=["Loneperiods"])
def create_loneperiod(loneperiod: LoneperiodCreate):
    """Skapa ny löneperiod - Requires API Key"""
    try:
        data = loneperiod.model_dump()
        # Convert dates to strings
        if 'start_date' in data:
            data['start_date'] = data['start_date'].isoformat()
        if 'end_date' in data:
            data['end_date'] = data['end_date'].isoformat()
        
        created = db_adapter.create_loneperiod(data)
        return created
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Kunde inte skapa löneperiod: {str(e)}")


@app.put("/api/v1/loneperiods/{loneperiod_id}", response_model=LoneperiodResponse,
         dependencies=[Depends(api_key_auth)], tags=["Loneperiods"])
def update_loneperiod(loneperiod_id: int, loneperiod: LoneperiodUpdate):
    """Uppdatera löneperiod - Requires API Key"""
    data = loneperiod.model_dump(exclude_unset=True)
    
    # Convert dates to strings
    if 'start_date' in data:
        data['start_date'] = data['start_date'].isoformat()
    if 'end_date' in data:
        data['end_date'] = data['end_date'].isoformat()
    
    updated = db_adapter.update_loneperiod(loneperiod_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Löneperiod {loneperiod_id} hittades inte")
    return updated


@app.get("/api/v1/loneperiods/{loneperiod_id}/progress", response_model=LoneperiodProgressResponse,
         dependencies=[Depends(api_key_auth)], tags=["Loneperiods"])
def get_loneperiod_progress(loneperiod_id: int):
    """Hämta framdrift för löneperiod - Requires API Key"""
    try:
        progress = db_adapter.get_loneperiod_progress(loneperiod_id)
        return progress
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fel vid hämtning: {str(e)}")


@app.post("/api/v1/loneperiods/{loneperiod_id}/activities", status_code=201,
          dependencies=[Depends(api_key_auth)], tags=["Loneperiods"])
def add_activities_to_loneperiod(loneperiod_id: int, request: AddActivitiesRequest):
    """Lägg till aktiviteter till löneperiod - Requires API Key"""
    try:
        added = db_adapter.add_activities_to_loneperiod(loneperiod_id, request.activity_ids)
        return {"message": f"Lade till {added} aktiviteter", "added_count": added}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fel vid tillägg: {str(e)}")


# ============================================================================
# LA INTEGRATION - DATA ENDPOINTS (AUTH REQUIRED)
# ============================================================================

@app.get("/api/v1/la/employees", response_model=List[LAEmployeeResponse],
         dependencies=[Depends(api_key_auth)], tags=["LA Integration - Data"])
def get_la_employees(
    org_kod: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(100, le=1000)
):
    """Hämta anställda från Firestore - Requires API Key"""
    try:
        employees = db_adapter.get_employees(
            org_kod=org_kod,
            status=status,
            limit=limit
        )
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fel vid hämtning: {str(e)}")


# ============================================================================
# v3.0 FELLISTOR ENDPOINTS (AUTH REQUIRED)
# ============================================================================

@app.get("/api/v1/la/fellistor/{loneperiod_id}", response_model=List[LACalculationErrorResponse],
         dependencies=[Depends(api_key_auth)], tags=["LA Integration - Fellistor"])
def get_fellistor(
    loneperiod_id: int,
    severity: Optional[str] = Query(None, pattern="^(error|warning|info)$"),
    visa_endast_obehandlade: bool = False,
    visa_endast_olosta: bool = False
):
    """Hämta fellista för löneperiod - Requires API Key"""
    try:
        errors = db_adapter.get_fellistor(
            loneperiod_id=loneperiod_id,
            severity=severity,
            visa_endast_obehandlade=visa_endast_obehandlade,
            visa_endast_olosta=visa_endast_olosta
        )
        return errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fel vid hämtning: {str(e)}")


@app.get("/api/v1/la/fellistor/{loneperiod_id}/summary", response_model=FellistaSummary,
         dependencies=[Depends(api_key_auth)], tags=["LA Integration - Fellistor"])
def get_fellista_summary(loneperiod_id: int):
    """Hämta sammanfattning av fellista - Requires API Key"""
    try:
        summary = db_adapter.get_fellista_summary(loneperiod_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fel vid hämtning: {str(e)}")


@app.patch("/api/v1/la/fellistor/{error_id}", response_model=LACalculationErrorResponse,
           dependencies=[Depends(api_key_auth)], tags=["LA Integration - Fellistor"])
def update_fellista_error(error_id: str, update: LACalculationErrorUpdate):
    """Uppdatera fel i fellistan - Requires API Key"""
    updated = db_adapter.update_fellista_error(error_id, update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail=f"Fel {error_id} hittades inte")
    return updated


# ============================================================================
# v3.0 KÖRNINGSSTATUS ENDPOINTS (AUTH REQUIRED)
# ============================================================================

@app.get("/api/v1/la/periods/{loneperiod_id}/korningsstatus", response_model=KorningsStatusResponse,
         dependencies=[Depends(api_key_auth)], tags=["LA Integration - Körningsstatus"])
def get_korningsstatus(loneperiod_id: int):
    """Hämta körningsstatus för löneperiod - Requires API Key"""
    status = db_adapter.get_korningsstatus(loneperiod_id)
    if not status:
        raise HTTPException(status_code=404, detail=f"Körningsstatus för {loneperiod_id} hittades inte")
    return status


@app.patch("/api/v1/la/periods/{loneperiod_id}/korningsstatus", response_model=KorningsStatusResponse,
           dependencies=[Depends(api_key_auth)], tags=["LA Integration - Körningsstatus"])
def update_korningsstatus(loneperiod_id: int, update: KorningsStatusUpdate):
    """Uppdatera körningsstatus - Requires API Key"""
    updated = db_adapter.update_korningsstatus(loneperiod_id, update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail=f"Körningsstatus för {loneperiod_id} hittades inte")
    return updated


# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 70)
    print("🔥 Löneprocess Digital Checklista API v3.0 - STAGING")
    print("=" * 70)
    print(f"Environment: Staging")
    print(f"Database: Firestore")
    print(f"Version: {API_VERSION}")
    print(f"Authentication: API Key Required (X-API-Key header)")
    print(f"Rate Limit: 60 requests/minute")
    
    print("\n📚 Swagger UI: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    print("💚 Health: http://localhost:8000/health")
    print("\n🔐 Note: API endpoints require X-API-Key header")
    print("=" * 70)
    print("Startar server...\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
