#!/usr/bin/env python3
"""
Löneprocess Digital Checklista API v3.0
Main application file with all endpoints
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional, List
import httpx

# Import från lokala moduler
from config import (
    API_TITLE, API_VERSION, API_DESCRIPTION,
    CORS_ORIGINS, CORS_ALLOW_CREDENTIALS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS,
    LA_USE_MOCK, LA_API_URL
)
from database import get_db, dict_from_row, init_database
from models import *


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


# ============================================================================
# HEALTH ENDPOINTS
# ============================================================================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "message": "Löneprocess Digital Checklista API v3.0",
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": API_VERSION,
        "service": "Löneprocess API v3.0"
    }


# ============================================================================
# ACTIVITIES ENDPOINTS
# ============================================================================

@app.get("/api/v1/activities", response_model=List[ActivityResponse], tags=["Activities"])
async def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    process: Optional[str] = None,
    role: Optional[str] = None,
    status: Optional[str] = None
):
    """Hämta aktiviteter med filtrering"""
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM activities WHERE 1=1"
        params = []
        
        if process:
            query += " AND process = ?"
            params.append(process)
        if role:
            query += " AND roll = ?"
            params.append(role)
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, skip])
        
        cursor.execute(query, params)
        return [dict_from_row(row) for row in cursor.fetchall()]


@app.get("/api/v1/activities/{activity_id}", response_model=ActivityResponse, tags=["Activities"])
async def get_activity(activity_id: int):
    """Hämta specifik aktivitet"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activities WHERE id = ?", (activity_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Aktivitet {activity_id} hittades inte")
        return dict_from_row(row)


@app.post("/api/v1/activities", response_model=ActivityResponse, status_code=201, tags=["Activities"])
async def create_activity(activity: ActivityCreate):
    """Skapa ny aktivitet"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO activities (
                process_nr, process, out_input, ska_inga_i_loneperiod, fas, roll,
                behov, effekten_vardet, extra_info, acceptans, feature_losning,
                priority, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            activity.process_nr, activity.process, activity.out_input,
            1 if activity.ska_inga_i_loneperiod else 0,
            activity.fas, activity.roll, activity.behov, activity.effekten_vardet,
            activity.extra_info, activity.acceptans, activity.feature_losning,
            activity.priority, activity.status
        ))
        conn.commit()
        cursor.execute("SELECT * FROM activities WHERE id = ?", (cursor.lastrowid,))
        return dict_from_row(cursor.fetchone())


@app.put("/api/v1/activities/{activity_id}", response_model=ActivityResponse, tags=["Activities"])
async def update_activity(activity_id: int, activity: ActivityUpdate):
    """Uppdatera aktivitet"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activities WHERE id = ?", (activity_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Aktivitet {activity_id} hittades inte")
        
        updates = []
        params = []
        for field, value in activity.model_dump(exclude_unset=True).items():
            if field == 'ska_inga_i_loneperiod':
                value = 1 if value else 0
            updates.append(f"{field} = ?")
            params.append(value)
        
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(activity_id)
            cursor.execute(f"UPDATE activities SET {', '.join(updates)} WHERE id = ?", params)
            conn.commit()
        
        cursor.execute("SELECT * FROM activities WHERE id = ?", (activity_id,))
        return dict_from_row(cursor.fetchone())


@app.delete("/api/v1/activities/{activity_id}", status_code=204, tags=["Activities"])
async def delete_activity(activity_id: int):
    """Ta bort aktivitet"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Aktivitet {activity_id} hittades inte")
        conn.commit()


# ============================================================================
# LONEPERIODS ENDPOINTS
# ============================================================================

@app.get("/api/v1/loneperiods", response_model=List[LoneperiodResponse], tags=["Loneperiods"])
async def get_loneperiods(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    year: Optional[int] = None
):
    """Hämta löneperioder"""
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM loneperiods WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        if year:
            query += " AND strftime('%Y', start_date) = ?"
            params.append(str(year))
        
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, skip])
        
        cursor.execute(query, params)
        return [dict_from_row(row) for row in cursor.fetchall()]


@app.get("/api/v1/loneperiods/{loneperiod_id}", response_model=LoneperiodResponse, tags=["Loneperiods"])
async def get_loneperiod(loneperiod_id: int):
    """Hämta specifik löneperiod"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM loneperiods WHERE id = ?", (loneperiod_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Löneperiod {loneperiod_id} hittades inte")
        return dict_from_row(row)


@app.post("/api/v1/loneperiods", response_model=LoneperiodResponse, status_code=201, tags=["Loneperiods"])
async def create_loneperiod(loneperiod: LoneperiodCreate):
    """Skapa ny löneperiod"""
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO loneperiods (name, start_date, end_date, status)
                VALUES (?, ?, ?, ?)
            """, (
                loneperiod.name,
                loneperiod.start_date.isoformat(),
                loneperiod.end_date.isoformat(),
                loneperiod.status
            ))
            conn.commit()
            cursor.execute("SELECT * FROM loneperiods WHERE id = ?", (cursor.lastrowid,))
            return dict_from_row(cursor.fetchone())
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Kunde inte skapa löneperiod: {str(e)}")


@app.put("/api/v1/loneperiods/{loneperiod_id}", response_model=LoneperiodResponse, tags=["Loneperiods"])
async def update_loneperiod(loneperiod_id: int, loneperiod: LoneperiodUpdate):
    """Uppdatera löneperiod"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM loneperiods WHERE id = ?", (loneperiod_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Löneperiod {loneperiod_id} hittades inte")
        
        updates = []
        params = []
        for field, value in loneperiod.model_dump(exclude_unset=True).items():
            if value is not None:
                if isinstance(value, date):
                    value = value.isoformat()
                updates.append(f"{field} = ?")
                params.append(value)
        
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(loneperiod_id)
            cursor.execute(f"UPDATE loneperiods SET {', '.join(updates)} WHERE id = ?", params)
            conn.commit()
        
        cursor.execute("SELECT * FROM loneperiods WHERE id = ?", (loneperiod_id,))
        return dict_from_row(cursor.fetchone())


@app.get("/api/v1/loneperiods/{loneperiod_id}/progress", response_model=LoneperiodProgressResponse, tags=["Loneperiods"])
async def get_loneperiod_progress(loneperiod_id: int):
    """Hämta framdrift för löneperiod"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM loneperiods WHERE id = ?", (loneperiod_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Löneperiod {loneperiod_id} hittades inte")
        
        cursor.execute("SELECT COUNT(*) as total FROM assignments WHERE loneperiod_id = ?", (loneperiod_id,))
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as completed FROM assignments WHERE loneperiod_id = ? AND is_completed = 1", (loneperiod_id,))
        completed = cursor.fetchone()['completed']
        
        completion_percentage = (completed / total * 100) if total > 0 else 0.0
        
        return {
            "loneperiod_id": loneperiod_id,
            "completion_percentage": round(completion_percentage, 2),
            "completed_count": completed,
            "total_count": total,
            "pending_count": total - completed
        }


@app.post("/api/v1/loneperiods/{loneperiod_id}/activities", status_code=201, tags=["Loneperiods"])
async def add_activities_to_loneperiod(loneperiod_id: int, request: AddActivitiesRequest):
    """Lägg till aktiviteter till löneperiod"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM loneperiods WHERE id = ?", (loneperiod_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Löneperiod {loneperiod_id} hittades inte")
        
        added = 0
        for activity_id in request.activity_ids:
            cursor.execute("SELECT * FROM assignments WHERE loneperiod_id = ? AND activity_id = ?",
                         (loneperiod_id, activity_id))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO assignments (loneperiod_id, activity_id) VALUES (?, ?)",
                             (loneperiod_id, activity_id))
                added += 1
        
        conn.commit()
        return {"message": f"Lade till {added} aktiviteter", "added_count": added}


# ============================================================================
# LA INTEGRATION - SYNC ENDPOINTS
# ============================================================================

@app.post("/api/v1/la/sync/employees", response_model=SyncResponse, tags=["LA Integration - Sync"])
async def sync_employees_from_la(org_kod: Optional[str] = Query(None)):
    """Synka anställda från LA"""
    started_at = datetime.now().isoformat()
    
    try:
        base_url = "http://localhost:8000" if LA_USE_MOCK else LA_API_URL
        async with httpx.AsyncClient() as client:
            params = {"org_kod": org_kod} if org_kod else {}
            response = await client.get(f"{base_url}/api/la-mock/v1/employees", params=params)
            response.raise_for_status()
            employees = response.json()
        
        with get_db() as conn:
            cursor = conn.cursor()
            synced_count = 0
            
            for emp in employees:
                cursor.execute("""
                    INSERT OR REPLACE INTO la_employees (
                        anstnr, fnamn, enamn, personnummer, org_kod, org_namn,
                        bef_kod, bef_namn, arbl, anstdat, avgdat, status,
                        heltidslon, syssgrad, last_synced_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    emp["anstnr"], emp.get("fnamn"), emp.get("enamn"), emp.get("personnummer"),
                    emp.get("org_kod"), emp.get("org_namn"), emp.get("bef_kod"), emp.get("bef_namn"),
                    emp.get("arbl"), emp.get("anstdat"), emp.get("avgdat"), emp.get("status"),
                    emp.get("heltidslon"), emp.get("syssgrad"), started_at
                ))
                synced_count += 1
            
            cursor.execute("""
                INSERT INTO la_sync_log (sync_type, status, records_synced, started_at, completed_at)
                VALUES (?, ?, ?, ?, ?)
            """, ("employees", "success", synced_count, started_at, datetime.now().isoformat()))
            
            conn.commit()
        
        return {
            "status": "success",
            "sync_type": "employees",
            "records_synced": synced_count,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO la_sync_log (sync_type, status, records_synced, error_message, started_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("employees", "failed", 0, str(e), started_at, datetime.now().isoformat()))
            conn.commit()
        
        raise HTTPException(status_code=500, detail=f"Sync misslyckades: {str(e)}")


# ============================================================================
# LA INTEGRATION - DATA ENDPOINTS
# ============================================================================

@app.get("/api/v1/la/employees", response_model=List[LAEmployeeResponse], tags=["LA Integration - Data"])
async def get_la_employees(
    org_kod: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(100, le=1000)
):
    """Hämta synkade anställda"""
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM la_employees WHERE 1=1"
        params = []
        
        if org_kod:
            query += " AND org_kod = ?"
            params.append(org_kod)
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        return [dict_from_row(row) for row in cursor.fetchall()]


# ============================================================================
# v3.0 FELLISTOR ENDPOINTS
# ============================================================================

@app.get("/api/v1/la/fellistor/{loneperiod_id}", response_model=List[LACalculationErrorResponse], tags=["LA Integration - Fellistor"])
async def get_fellistor(
    loneperiod_id: int,
    severity: Optional[str] = Query(None, regex="^(error|warning|info)$"),
    visa_endast_obehandlade: bool = False,
    visa_endast_olosta: bool = False
):
    """Hämta fellista för löneperiod"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM loneperiods WHERE id = ?", (loneperiod_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Löneperiod {loneperiod_id} hittades inte")
        
        query = "SELECT * FROM la_calculation_errors WHERE loneperiod_id = ?"
        params = [loneperiod_id]
        
        if severity:
            query += " AND severity = ?"
            params.append(severity)
        if visa_endast_obehandlade:
            query += " AND behandlat = 0"
        if visa_endast_olosta:
            query += " AND is_resolved = 0"
        
        query += " ORDER BY severity DESC, detected_at DESC"
        
        cursor.execute(query, params)
        return [dict_from_row(row) for row in cursor.fetchall()]


@app.get("/api/v1/la/fellistor/{loneperiod_id}/summary", response_model=FellistaSummary, tags=["LA Integration - Fellistor"])
async def get_fellista_summary(loneperiod_id: int):
    """Hämta sammanfattning av fellista"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM loneperiods WHERE id = ?", (loneperiod_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Löneperiod {loneperiod_id} hittades inte")
        
        cursor.execute("""
            SELECT severity, COUNT(*) as count
            FROM la_calculation_errors
            WHERE loneperiod_id = ?
            GROUP BY severity
        """, (loneperiod_id,))
        severity_counts = {row["severity"]: row["count"] for row in cursor.fetchall()}
        
        cursor.execute("""
            SELECT severity, COUNT(*) as count
            FROM la_calculation_errors
            WHERE loneperiod_id = ? AND is_resolved = 0
            GROUP BY severity
        """, (loneperiod_id,))
        unresolved_counts = {row["severity"]: row["count"] for row in cursor.fetchall()}
        
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM la_calculation_errors
            WHERE loneperiod_id = ? AND behandlat = 0
        """, (loneperiod_id,))
        obehandlade = cursor.fetchone()["count"]
        
        cursor.execute("""
            SELECT error_code, COUNT(*) as count
            FROM la_calculation_errors
            WHERE loneperiod_id = ?
            GROUP BY error_code
            ORDER BY count DESC
        """, (loneperiod_id,))
        errors_by_code = {row["error_code"]: row["count"] for row in cursor.fetchall()}
        
        return {
            "loneperiod_id": loneperiod_id,
            "total_errors": severity_counts.get("error", 0),
            "total_warnings": severity_counts.get("warning", 0),
            "total_info": severity_counts.get("info", 0),
            "unresolved_errors": unresolved_counts.get("error", 0),
            "unresolved_warnings": unresolved_counts.get("warning", 0),
            "obehandlade": obehandlade,
            "errors_by_code": errors_by_code
        }


@app.patch("/api/v1/la/fellistor/{error_id}", response_model=LACalculationErrorResponse, tags=["LA Integration - Fellistor"])
async def update_fellista_error(error_id: int, update: LACalculationErrorUpdate):
    """Uppdatera fel i fellistan"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM la_calculation_errors WHERE id = ?", (error_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Fel {error_id} hittades inte")
        
        updates = []
        params = []
        
        if update.behandlat is not None:
            updates.append("behandlat = ?")
            params.append(1 if update.behandlat else 0)
        
        if update.is_resolved is not None:
            updates.append("is_resolved = ?")
            params.append(1 if update.is_resolved else 0)
            if update.is_resolved:
                updates.append("resolved_at = ?")
                params.append(datetime.now().isoformat())
        
        if update.notes is not None:
            updates.append("notes = ?")
            params.append(update.notes)
        
        if updates:
            params.append(error_id)
            cursor.execute(f"UPDATE la_calculation_errors SET {', '.join(updates)} WHERE id = ?", params)
            conn.commit()
        
        cursor.execute("SELECT * FROM la_calculation_errors WHERE id = ?", (error_id,))
        return dict_from_row(cursor.fetchone())


# ============================================================================
# v3.0 KÖRNINGSSTATUS ENDPOINTS
# ============================================================================

@app.get("/api/v1/la/periods/{loneperiod_id}/korningsstatus", response_model=KorningsStatusResponse, tags=["LA Integration - Körningsstatus"])
async def get_korningsstatus(loneperiod_id: int):
    """Hämta körningsstatus för löneperiod"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT lp.*, lpm.*
            FROM loneperiods lp
            LEFT JOIN la_period_mappings lpm ON lp.id = lpm.loneperiod_id
            WHERE lp.id = ?
        """, (loneperiod_id,))
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Löneperiod {loneperiod_id} hittades inte")
        
        result = dict_from_row(row)
        
        provlon_status = result.get("provlon_status", "ej_startad")
        slutlon_status = result.get("slutlon_status", "ej_startad")
        
        can_start_provlon = provlon_status in ["ej_startad", "fel"]
        can_start_slutlon = (provlon_status == "klar" and slutlon_status in ["ej_startad", "fel"])
        
        return {
            "loneperiod_id": loneperiod_id,
            "la_period_code": result.get("la_period_code", ""),
            "provlon_status": provlon_status,
            "provlon_started_at": result.get("provlon_started_at"),
            "provlon_completed_at": result.get("provlon_completed_at"),
            "slutlon_status": slutlon_status,
            "slutlon_started_at": result.get("slutlon_started_at"),
            "slutlon_completed_at": result.get("slutlon_completed_at"),
            "can_start_provlon": can_start_provlon,
            "can_start_slutlon": can_start_slutlon
        }


@app.patch("/api/v1/la/periods/{loneperiod_id}/korningsstatus", response_model=KorningsStatusResponse, tags=["LA Integration - Körningsstatus"])
async def update_korningsstatus(loneperiod_id: int, update: KorningsStatusUpdate):
    """Uppdatera körningsstatus"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM la_period_mappings WHERE loneperiod_id = ?", (loneperiod_id,))
        
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Period mapping för {loneperiod_id} hittades inte")
        
        updates = []
        params = []
        now = datetime.now().isoformat()
        
        if update.provlon_status:
            updates.append("provlon_status = ?")
            params.append(update.provlon_status)
            
            if update.provlon_status == "startad":
                updates.append("provlon_started_at = ?")
                params.append(now)
            elif update.provlon_status in ["klar", "fel"]:
                updates.append("provlon_completed_at = ?")
                params.append(now)
                updates.append("provlon_run = 1")
        
        if update.slutlon_status:
            updates.append("slutlon_status = ?")
            params.append(update.slutlon_status)
            
            if update.slutlon_status == "startad":
                updates.append("slutlon_started_at = ?")
                params.append(now)
            elif update.slutlon_status in ["klar", "fel"]:
                updates.append("slutlon_completed_at = ?")
                params.append(now)
                updates.append("slutlon_run = 1")
        
        if updates:
            params.append(loneperiod_id)
            cursor.execute(f"UPDATE la_period_mappings SET {', '.join(updates)} WHERE loneperiod_id = ?", params)
            conn.commit()
        
        return await get_korningsstatus(loneperiod_id)


# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 70)
    print("🚀 Löneprocess Digital Checklista API v3.0")
    print("=" * 70)
    
    init_database()
    
    print("\n📚 Swagger UI: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    print("💚 Health: http://localhost:8000/health")
    print("\n" + "=" * 70)
    print("Startar server...\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
