"""
Database models and initialization for Löneprocess API v3.0
Contains all table definitions and sample data
"""
import sqlite3
from contextlib import contextmanager
from config import DB_NAME


@contextmanager
def get_db():
    """Database connection context manager"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def dict_from_row(row):
    """Convert sqlite3.Row to dict"""
    if row is None:
        return None
    return {key: row[key] for key in row.keys()}


def init_database():
    """Initialize database with all tables and sample data"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # ====================================================================
        # ORIGINAL TABLES
        # ====================================================================
        
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
        
        # ====================================================================
        # LA INTEGRATION TABLES (v2.0)
        # ====================================================================
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS la_employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anstnr TEXT UNIQUE NOT NULL,
                fnamn TEXT,
                enamn TEXT,
                personnummer TEXT,
                org_kod TEXT,
                org_namn TEXT,
                bef_kod TEXT,
                bef_namn TEXT,
                arbl TEXT,
                anstdat TEXT,
                avgdat TEXT,
                status TEXT DEFAULT 'active',
                heltidslon REAL,
                syssgrad REAL,
                last_synced_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS la_period_mappings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                loneperiod_id INTEGER NOT NULL,
                la_period_code TEXT NOT NULL,
                la_start_date TEXT,
                la_end_date TEXT,
                la_status TEXT,
                utbetalningsdag TEXT,
                provlon_run INTEGER DEFAULT 0,
                slutlon_run INTEGER DEFAULT 0,
                provlon_status TEXT DEFAULT 'ej_startad',
                provlon_started_at TEXT,
                provlon_completed_at TEXT,
                slutlon_status TEXT DEFAULT 'ej_startad',
                slutlon_started_at TEXT,
                slutlon_completed_at TEXT,
                is_synced INTEGER DEFAULT 0,
                last_synced_at TEXT,
                FOREIGN KEY (loneperiod_id) REFERENCES loneperiods(id),
                UNIQUE(loneperiod_id, la_period_code)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS la_absences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anstnr TEXT NOT NULL,
                absence_code TEXT,
                absence_type TEXT,
                absence_description TEXT,
                start_date TEXT,
                end_date TEXT,
                hours REAL,
                days REAL,
                loneperiod_id INTEGER,
                last_synced_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (loneperiod_id) REFERENCES loneperiods(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS la_vacation_balances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anstnr TEXT NOT NULL,
                semratt REAL,
                semspar REAL,
                uttagna REAL,
                kvar REAL,
                semlongr REAL,
                as_of_date TEXT,
                last_synced_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(anstnr, as_of_date)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS la_benefits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anstnr TEXT NOT NULL,
                benefit_type TEXT,
                benefit_code TEXT,
                benefit_value REAL,
                start_date TEXT,
                end_date TEXT,
                last_synced_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS la_tax_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anstnr TEXT NOT NULL,
                skattetabell TEXT,
                skattekod TEXT,
                avdragskod_1 TEXT,
                avdragskod_2 TEXT,
                avdragskod_3 TEXT,
                fackavgift_mottagare TEXT,
                fackavgift_procent REAL,
                last_synced_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(anstnr)
            )
        """)
        
        # ====================================================================
        # v3.0 TABLES - FELLISTOR & KÖRNINGSSTATUS
        # ====================================================================
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS la_calculation_errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                loneperiod_id INTEGER,
                anstnr TEXT,
                error_code TEXT,
                error_message TEXT,
                field_name TEXT,
                severity TEXT,
                is_resolved INTEGER DEFAULT 0,
                behandlat INTEGER DEFAULT 0,
                detected_at TEXT,
                resolved_at TEXT,
                notes TEXT,
                FOREIGN KEY (loneperiod_id) REFERENCES loneperiods(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS la_sync_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sync_type TEXT NOT NULL,
                status TEXT,
                records_synced INTEGER DEFAULT 0,
                error_message TEXT,
                started_at TEXT,
                completed_at TEXT
            )
        """)
        
        # ====================================================================
        # SAMPLE DATA
        # ====================================================================
        
        cursor.execute("SELECT COUNT(*) as count FROM activities")
        if cursor.fetchone()['count'] == 0:
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
            
            cursor.executemany("""
                INSERT INTO assignments (loneperiod_id, activity_id, is_completed)
                VALUES (?, ?, ?)
            """, [
                (1, 1, 1), (1, 2, 1), (1, 3, 0), (1, 4, 0),
            ])
        
        conn.commit()
        print("✓ Database initialized successfully with v3.0 schema")
