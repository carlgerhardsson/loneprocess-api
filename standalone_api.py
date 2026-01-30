#!/usr/bin/env python3
"""
Löneprocess Digital Checklista API - Standalone version
Komplett FastAPI app med SQLite databas och automatisk OpenAPI/Swagger UI
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
import sqlite3
import json
from contextlib import contextmanager

# ============================================================================
# DATABASE SETUP
# ============================================================================

DB_NAME = "loneprocess.db"

@contextmanager
def get_db():
    """Database connection context manager"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """Initialize database with tables and sample data"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Create activities table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                process_nr TEXT,
                process TEXT,
                out_input TEXT,
                ska_inga_i_loneperiod INTEGER DEFAULT 0,
                fas INTEGER,
                roll TEXT,
                behov TEXT,
                effekten_vardet TEXT,
                extra_info TEXT,
                acceptans TEXT,
                feature_losning TEXT,
                priority INTEGER,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            )
        """)
        
        # Create loneperiods table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS loneperiods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT DEFAULT 'planned',
                completion_percentage REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            )
        """)
        
        # Create assignments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                loneperiod_id INTEGER NOT NULL,
                activity_id INTEGER NOT NULL,
                is_completed INTEGER DEFAULT 0,
                completed_at TEXT,
                notes TEXT,
                FOREIGN KEY (loneperiod_id) REFERENCES loneperiods(id),
                FOREIGN KEY (activity_id) REFERENCES activities(id)
            )
        """)
        
        # Check if we need to add sample data
        cursor.execute("SELECT COUNT(*) as count FROM activities")
        if cursor.fetchone()['count'] == 0:
            # Insert sample activities
            sample_activities = [
                ('10.1', 'Anställningsprocess', 'Nya anställningar', 1, None, 'Lönespecialist', 
                 'Registera och komplettera nya anställningar', 'Inför varje löneperiod', None,
                 'Jag är nöjd när anställningarna har kommit in', 'Genom att göra si eller så…', 1, 'pending'),
                ('10.2', 'Anställningsprocess', 'Anställningsförändringar', 1, None, 'Lönespecialist',
                 'Registera och komplettera anställningsförändringar', 'Inför varje löneperiod', None,
                 None, None, 1, 'pending'),
                ('10.3', 'Input till lön', 'Ärenden som kommer via processer', 1, None, 'Lönespecialist',
                 'Hantera ärenden som kommer via processer', 'Inför varje löneperiod', None,
                 None, None, 1, 'in_progress'),
                ('10.4', 'Input till lön', 'Schemabyten', 0, None, 'Lönespecialist',
                 'Hantera schemabyten', 'Inför varje löneperiod', None,
                 None, None, 2, 'pending'),
                ('10.5', 'Input till lön', 'Bevakningar', 0, None, 'Lönespecialist',
                 'Kontrollera och åtgärda bevakningar', 'Inför varje löneperiod', None,
                 None, None, 2, 'pending'),
            ]
            
            cursor.executemany("""
                INSERT INTO activities (
                    process_nr, process, out_input, ska_inga_i_loneperiod, fas, roll,
                    behov, effekten_vardet, extra_info, acceptans, feature_losning,
                    priority, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, sample_activities)
            
        # Check if we need to add sample loneperiods
        cursor.execute("SELECT COUNT(*) as count FROM loneperiods")
        if cursor.fetchone()['count'] == 0:
            sample_periods = [
                ('Januari 2026', '2026-01-01', '2026-01-31', 'active', 75.5),
                ('Februari 2026', '2026-02-01', '2026-02-28', 'planned', 0.0),
                ('Mars 2026', '2026-03-01', '2026-03-31', 'planned', 0.0),
            ]
            
            cursor.executemany("""
                INSERT INTO loneperiods (name, start_date, end_date, status, completion_percentage)
                VALUES (?, ?, ?, ?, ?)
            """, sample_periods)
            
            # Add some assignments
            cursor.executemany("""
                INSERT INTO assignments (loneperiod_id, activity_id, is_completed)
                VALUES (?, ?, ?)
            """, [
                (1, 1, 1), (1, 2, 1), (1, 3, 0), (1, 4, 0),
            ])
        
        conn.commit()
        print("✓ Database initialized successfully")

# ============================================================================
# PYDANTIC MODELS (SCHEMAS)
# ============================================================================

class ActivityBase(BaseModel):
    process_nr: Optional[str] = Field(None, max_length=50, description="Processnummer (t.ex. '10.1')")
    process: Optional[str] = Field(None, max_length=200, description="Processnamn")
    out_input: Optional[str] = Field(None, max_length=500, description="Aktivitetsbeskrivning")
    ska_inga_i_loneperiod: bool = Field(False, description="Om aktiviteten ska ingå i löneperiod")
    fas: Optional[int] = Field(None, description="Fasnummer")
    roll: Optional[str] = Field(None, max_length=100, description="Roll (t.ex. 'Lönespecialist')")
    behov: Optional[str] = Field(None, description="Beskrivning av behov")
    effekten_vardet: Optional[str] = Field(None, description="Effekten värdet (varför, när, hur ofta)")
    extra_info: Optional[str] = Field(None, description="Extra information")
    acceptans: Optional[str] = Field(None, description="Acceptanskriterier")
    feature_losning: Optional[str] = Field(None, description="Teknisk lösning")
    priority: Optional[int] = Field(None, ge=1, le=5, description="Prioritet (1-5)")
    status: str = Field("pending", description="Status: pending, in_progress, completed")

    class Config:
        json_schema_extra = {
            "example": {
                "process_nr": "10.9",
                "out_input": "Ny aktivitet",
                "roll": "Lönespecialist",
                "ska_inga_i_loneperiod": True,
                "priority": 1
            }
        }

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    process_nr: Optional[str] = None
    process: Optional[str] = None
    out_input: Optional[str] = None
    ska_inga_i_loneperiod: Optional[bool] = None
    fas: Optional[int] = None
    roll: Optional[str] = None
    behov: Optional[str] = None
    effekten_vardet: Optional[str] = None
    extra_info: Optional[str] = None
    acceptans: Optional[str] = None
    feature_losning: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "completed",
                "priority": 2
            }
        }

class ActivityResponse(ActivityBase):
    id: int
    created_at: str
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True

class LoneperiodBase(BaseModel):
    name: str = Field(..., max_length=200, description="Löneperiodens namn")
    start_date: date = Field(..., description="Startdatum")
    end_date: date = Field(..., description="Slutdatum")
    status: str = Field("planned", description="Status: planned, active, closed")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "April 2026",
                "start_date": "2026-04-01",
                "end_date": "2026-04-30",
                "status": "planned"
            }
        }

class LoneperiodCreate(LoneperiodBase):
    pass

class LoneperiodUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    completion_percentage: Optional[float] = Field(None, ge=0, le=100)

class LoneperiodResponse(LoneperiodBase):
    id: int
    completion_percentage: float
    created_at: str
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True

class LoneperiodProgressResponse(BaseModel):
    loneperiod_id: int
    completion_percentage: float
    completed_count: int
    total_count: int
    pending_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "loneperiod_id": 1,
                "completion_percentage": 75.5,
                "completed_count": 30,
                "total_count": 40,
                "pending_count": 10
            }
        }

class AddActivitiesRequest(BaseModel):
    activity_ids: List[int] = Field(..., description="Lista med aktivitets-ID:n")

    class Config:
        json_schema_extra = {
            "example": {
                "activity_ids": [1, 2, 3, 4, 5]
            }
        }

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="Löneprocess Digital Checklista API",
    version="1.0.0",
    description="""
# Löneprocess Digital Checklista API

Detta API stödjer hantering av löneprocessaktiviteter och löneperioder.

## Huvudfunktioner

* **Aktivitetshantering** - Skapa, uppdatera och spåra löneprocessaktiviteter
* **Löneperioder** - Hantera löneperioder och deras framdrift  
* **Progress Tracking** - Få översikt över slutförda och pågående aktiviteter
* **Bemanningshantering** - Hantera användare och bemanningsområden

## Autentisering

API:et använder Bearer Token autentisering (valfritt i denna version).

## Teknisk Stack

- **Framework**: FastAPI
- **Database**: SQLite
- **Format**: JSON

## Kom igång

Testa API:et direkt här i Swagger UI genom att klicka på endpoints och "Try it out"!
    """,
    contact={
        "name": "Löneprocess Support",
        "email": "support@loneprocess.se"
    },
    license_info={
        "name": "Proprietary"
    },
    openapi_tags=[
        {
            "name": "Activities",
            "description": "Hantering av löneprocessaktiviteter"
        },
        {
            "name": "Loneperiods", 
            "description": "Hantering av löneperioder och framdrift"
        },
        {
            "name": "Health",
            "description": "API health check"
        }
    ]
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def dict_from_row(row):
    """Convert sqlite3.Row to dict"""
    return dict(zip(row.keys(), row)) if row else None

# ============================================================================
# ENDPOINTS - HEALTH
# ============================================================================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint med API information"""
    return {
        "message": "Löneprocess Digital Checklista API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returnerar API:ets hälsostatus och version.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Löneprocess Digital Checklista API",
        "database": "SQLite"
    }

# ============================================================================
# ENDPOINTS - ACTIVITIES
# ============================================================================

@app.get(
    "/api/v1/activities",
    response_model=List[ActivityResponse],
    tags=["Activities"],
    summary="Hämta aktiviteter",
    description="Hämta en lista av löneprocessaktiviteter med valfri filtrering på process, roll och status."
)
async def get_activities(
    skip: int = Query(0, ge=0, description="Antal att hoppa över för paginering"),
    limit: int = Query(100, ge=1, le=1000, description="Max antal resultat"),
    process: Optional[str] = Query(None, description="Filtrera på process"),
    role: Optional[str] = Query(None, description="Filtrera på roll"),
    status: Optional[str] = Query(None, description="Filtrera på status (pending, in_progress, completed)")
):
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
        rows = cursor.fetchall()
        
        return [dict_from_row(row) for row in rows]

@app.get(
    "/api/v1/activities/{activity_id}",
    response_model=ActivityResponse,
    tags=["Activities"],
    summary="Hämta specifik aktivitet",
    description="Hämta en aktivitet baserat på ID."
)
async def get_activity(activity_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activities WHERE id = ?", (activity_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Aktivitet med ID {activity_id} hittades inte")
        
        return dict_from_row(row)

@app.post(
    "/api/v1/activities",
    response_model=ActivityResponse,
    status_code=201,
    tags=["Activities"],
    summary="Skapa ny aktivitet",
    description="Skapa en ny löneprocessaktivitet."
)
async def create_activity(activity: ActivityCreate):
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
        activity_id = cursor.lastrowid
        
        cursor.execute("SELECT * FROM activities WHERE id = ?", (activity_id,))
        return dict_from_row(cursor.fetchone())

@app.put(
    "/api/v1/activities/{activity_id}",
    response_model=ActivityResponse,
    tags=["Activities"],
    summary="Uppdatera aktivitet",
    description="Uppdatera en befintlig aktivitet."
)
async def update_activity(activity_id: int, activity: ActivityUpdate):
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Check if exists
        cursor.execute("SELECT * FROM activities WHERE id = ?", (activity_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Aktivitet med ID {activity_id} hittades inte")
        
        # Build update query
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
            
            query = f"UPDATE activities SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
        
        cursor.execute("SELECT * FROM activities WHERE id = ?", (activity_id,))
        return dict_from_row(cursor.fetchone())

@app.delete(
    "/api/v1/activities/{activity_id}",
    status_code=204,
    tags=["Activities"],
    summary="Ta bort aktivitet",
    description="Ta bort en aktivitet."
)
async def delete_activity(activity_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Aktivitet med ID {activity_id} hittades inte")
        
        conn.commit()
        return None

# ============================================================================
# ENDPOINTS - LONEPERIODS
# ============================================================================

@app.get(
    "/api/v1/loneperiods",
    response_model=List[LoneperiodResponse],
    tags=["Loneperiods"],
    summary="Hämta löneperioder",
    description="Hämta alla löneperioder med valfri filtrering."
)
async def get_loneperiods(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None, description="Filtrera på status (planned, active, closed)"),
    year: Optional[int] = Query(None, description="Filtrera på år")
):
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
        rows = cursor.fetchall()
        
        return [dict_from_row(row) for row in rows]

@app.get(
    "/api/v1/loneperiods/{loneperiod_id}",
    response_model=LoneperiodResponse,
    tags=["Loneperiods"],
    summary="Hämta specifik löneperiod"
)
async def get_loneperiod(loneperiod_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM loneperiods WHERE id = ?", (loneperiod_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Löneperiod med ID {loneperiod_id} hittades inte")
        
        return dict_from_row(row)

@app.post(
    "/api/v1/loneperiods",
    response_model=LoneperiodResponse,
    status_code=201,
    tags=["Loneperiods"],
    summary="Skapa ny löneperiod"
)
async def create_loneperiod(loneperiod: LoneperiodCreate):
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
            loneperiod_id = cursor.lastrowid
            
            cursor.execute("SELECT * FROM loneperiods WHERE id = ?", (loneperiod_id,))
            return dict_from_row(cursor.fetchone())
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail=f"En löneperiod med namnet '{loneperiod.name}' finns redan")

@app.put(
    "/api/v1/loneperiods/{loneperiod_id}",
    response_model=LoneperiodResponse,
    tags=["Loneperiods"],
    summary="Uppdatera löneperiod"
)
async def update_loneperiod(loneperiod_id: int, loneperiod: LoneperiodUpdate):
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM loneperiods WHERE id = ?", (loneperiod_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Löneperiod med ID {loneperiod_id} hittades inte")
        
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
            
            query = f"UPDATE loneperiods SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
        
        cursor.execute("SELECT * FROM loneperiods WHERE id = ?", (loneperiod_id,))
        return dict_from_row(cursor.fetchone())

@app.get(
    "/api/v1/loneperiods/{loneperiod_id}/progress",
    response_model=LoneperiodProgressResponse,
    tags=["Loneperiods"],
    summary="Hämta framdrift",
    description="Hämta framdriftsinformation för en löneperiod."
)
async def get_loneperiod_progress(loneperiod_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Verify loneperiod exists
        cursor.execute("SELECT * FROM loneperiods WHERE id = ?", (loneperiod_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Löneperiod med ID {loneperiod_id} hittades inte")
        
        # Get counts
        cursor.execute("""
            SELECT COUNT(*) as total FROM assignments WHERE loneperiod_id = ?
        """, (loneperiod_id,))
        total = cursor.fetchone()['total']
        
        cursor.execute("""
            SELECT COUNT(*) as completed FROM assignments 
            WHERE loneperiod_id = ? AND is_completed = 1
        """, (loneperiod_id,))
        completed = cursor.fetchone()['completed']
        
        completion_percentage = (completed / total * 100) if total > 0 else 0.0
        
        return {
            "loneperiod_id": loneperiod_id,
            "completion_percentage": round(completion_percentage, 2),
            "completed_count": completed,
            "total_count": total,
            "pending_count": total - completed
        }

@app.post(
    "/api/v1/loneperiods/{loneperiod_id}/activities",
    status_code=201,
    tags=["Loneperiods"],
    summary="Lägg till aktiviteter",
    description="Lägg till aktiviteter till en löneperiod."
)
async def add_activities_to_loneperiod(loneperiod_id: int, request: AddActivitiesRequest):
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Verify loneperiod exists
        cursor.execute("SELECT * FROM loneperiods WHERE id = ?", (loneperiod_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Löneperiod med ID {loneperiod_id} hittades inte")
        
        added = 0
        for activity_id in request.activity_ids:
            # Check if already exists
            cursor.execute("""
                SELECT * FROM assignments 
                WHERE loneperiod_id = ? AND activity_id = ?
            """, (loneperiod_id, activity_id))
            
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO assignments (loneperiod_id, activity_id)
                    VALUES (?, ?)
                """, (loneperiod_id, activity_id))
                added += 1
        
        conn.commit()
        
        return {
            "message": f"Lade till {added} aktiviteter till löneperiod",
            "added_count": added
        }

# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 70)
    print("🚀 Löneprocess Digital Checklista API")
    print("=" * 70)
    
    # Initialize database
    init_database()
    
    print("\n📚 Swagger UI kommer att vara tillgänglig på:")
    print("   http://localhost:8000/docs")
    print("\n📖 ReDoc kommer att vara tillgänglig på:")
    print("   http://localhost:8000/redoc")
    print("\n🔍 OpenAPI JSON:")
    print("   http://localhost:8000/openapi.json")
    print("\n💚 Health Check:")
    print("   http://localhost:8000/health")
    print("\n" + "=" * 70)
    print("Startar server...\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
