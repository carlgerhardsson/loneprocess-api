#!/usr/bin/env python3
"""
Firestore Test Data Seeder
Generates realistic Swedish test data for staging environment
"""
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict
import random
from pathlib import Path

# Setup Firebase - find credentials automatically
credentials_dir = Path(__file__).parent / "credentials"
credential_files = list(credentials_dir.glob("*.json"))

if not credential_files:
    print("❌ ERROR: No service account key found in credentials/")
    print("Please download serviceAccountKey.json from Firebase Console")
    sys.exit(1)

# Use the first .json file found
CREDENTIALS_PATH = str(credential_files[0])
print(f"✓ Using credentials: {CREDENTIALS_PATH}")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIALS_PATH

from firebase_admin import credentials, firestore, initialize_app

# Initialize Firebase (only if not already initialized)
try:
    initialize_app(credentials.Certificate(CREDENTIALS_PATH))
except ValueError:
    pass  # Already initialized

db = firestore.client()


# ============================================================================
# DATA GENERATORS
# ============================================================================

SWEDISH_FIRST_NAMES = [
    "Anna", "Erik", "Maria", "Lars", "Karin", "Per", "Emma", "Johan", "Sara", "Anders",
    "Linda", "Karl", "Eva", "Peter", "Kristina", "Mikael", "Annika", "Magnus", "Lena", "Mattias",
    "Helena", "Martin", "Susanne", "Fredrik", "Kerstin", "Niklas", "Malin", "Jonas", "Ingrid", "Daniel",
    "Birgitta", "Henrik", "Carina", "Patrik", "Monica", "Stefan", "Inger", "Björn", "Anette", "Torbjörn",
    "Margareta", "Andreas", "Gunilla", "Håkan", "Katarina", "Bengt", "Ulla", "Sven", "Marie", "Göran"
]

SWEDISH_LAST_NAMES = [
    "Andersson", "Johansson", "Karlsson", "Nilsson", "Eriksson", "Larsson", "Olsson", "Persson", "Svensson", "Gustafsson",
    "Pettersson", "Jonsson", "Jansson", "Hansson", "Bengtsson", "Jönsson", "Lindberg", "Jakobsson", "Magnusson", "Olofsson",
    "Lindström", "Lindqvist", "Lindgren", "Axelsson", "Berg", "Bergström", "Lundberg", "Lind", "Lundgren", "Lundqvist",
    "Mattsson", "Berglund", "Fredriksson", "Sandberg", "Henriksson", "Forsberg", "Sjöberg", "Wallin", "Ali", "Holm"
]

ORG_UNITS = [
    {"kod": "1000", "namn": "Ekonomi"},
    {"kod": "1100", "namn": "Ekonomi - Redovisning"},
    {"kod": "1200", "namn": "Ekonomi - Löneadministration"},
    {"kod": "2000", "namn": "IT"},
    {"kod": "2100", "namn": "IT - Systemutveckling"},
    {"kod": "2200", "namn": "IT - Support"},
    {"kod": "3000", "namn": "HR"},
    {"kod": "3100", "namn": "HR - Rekrytering"},
    {"kod": "3200", "namn": "HR - Personaladministration"},
    {"kod": "4000", "namn": "Försäljning"},
    {"kod": "5000", "namn": "Produktion"},
]

BEFATTNINGAR = [
    {"kod": "100", "namn": "VD"},
    {"kod": "200", "namn": "Chef"},
    {"kod": "300", "namn": "Ekonom"},
    {"kod": "400", "namn": "IT-specialist"},
    {"kod": "500", "namn": "HR-specialist"},
    {"kod": "600", "namn": "Säljare"},
    {"kod": "700", "namn": "Produktionsledare"},
    {"kod": "800", "namn": "Administratör"},
]

ERROR_CODES = {
    "E301": "Skattetabell saknas",
    "E302": "Felaktig löneart",
    "E303": "Semesterlöneskuld felaktig",
    "E304": "Tidsrapportering saknas",
    "E305": "Ob-tillägg saknas",
    "W105": "Avvikande sysselsättningsgrad",
    "W106": "Många övertidstimmar",
    "W107": "Semestersaldo lågt",
    "W108": "Fler än 40 timmar per vecka",
    "I201": "Ny anställd i perioden",
    "I202": "Anställning upphör inom 30 dagar",
    "I203": "Första lönen för denna anställd",
}


def generate_employee(anstnr: int) -> Dict:
    """Generate realistic Swedish employee"""
    fnamn = random.choice(SWEDISH_FIRST_NAMES)
    enamn = random.choice(SWEDISH_LAST_NAMES)
    org = random.choice(ORG_UNITS)
    bef = random.choice(BEFATTNINGAR)
    
    # Generate realistic personnummer (YYYYMMDD-XXXX)
    year = random.randint(1960, 2005)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    serial = random.randint(1000, 9999)
    personnummer = f"{year}{month:02d}{day:02d}-{serial}"
    
    # Employment date (within last 5 years or older)
    anstdat = (datetime.now() - timedelta(days=random.randint(0, 1825))).strftime("%Y-%m-%d")
    
    # Salary (20000 - 80000 SEK)
    heltidslon = random.randint(20000, 80000)
    
    # Employment level (50%, 75%, 100%, etc)
    syssgrad = random.choice([50, 75, 80, 90, 100])
    
    # Status (most active, some inactive)
    status = "active" if random.random() > 0.1 else "inactive"
    
    return {
        "anstnr": str(anstnr),
        "fnamn": fnamn,
        "enamn": enamn,
        "personnummer": personnummer,
        "org_kod": org["kod"],
        "org_namn": org["namn"],
        "bef_kod": bef["kod"],
        "bef_namn": bef["namn"],
        "arbl": "A" if random.random() > 0.2 else "T",  # Arbetstidsförkortning
        "anstdat": anstdat,
        "avgdat": None,  # Most employees still employed
        "status": status,
        "heltidslon": heltidslon,
        "syssgrad": syssgrad,
        "last_synced_at": datetime.now().isoformat()
    }


def generate_loneperiod(year: int, month: int) -> Dict:
    """Generate löneperiod"""
    period_id = f"{year}{month:02d}"
    month_names_sv = [
        "", "Januari", "Februari", "Mars", "April", "Maj", "Juni",
        "Juli", "Augusti", "September", "Oktober", "November", "December"
    ]
    
    # Calculate start and end dates
    from calendar import monthrange
    last_day = monthrange(year, month)[1]
    start_date = f"{year}-{month:02d}-01"
    end_date = f"{year}-{month:02d}-{last_day}"
    
    # Status based on date
    now = datetime.now()
    period_end = datetime(year, month, last_day)
    
    if period_end < now - timedelta(days=30):
        status = "completed"
        completion = 100.0
    elif period_end < now:
        status = "active"
        completion = random.uniform(50, 95)
    else:
        status = "upcoming"
        completion = 0.0
    
    return {
        "id": period_id,
        "name": f"{month_names_sv[month]} {year}",
        "start_date": start_date,
        "end_date": end_date,
        "status": status,
        "completion_percentage": round(completion, 2),
        "year": year,
        "month": month,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    }


def generate_activity(activity_id: int) -> Dict:
    """Generate activity"""
    processes = [
        ("10.1", "Anställningsprocess"),
        ("10.2", "Löneberäkning"),
        ("10.3", "Attestering"),
        ("20.1", "Rapportering"),
        ("20.2", "Kontroll"),
        ("30.1", "Utbetalning"),
    ]
    
    rolls = ["Lönechef", "Löneadministratör", "Ekonomiassistent", "Controller"]
    
    process_nr, process = random.choice(processes)
    roll = random.choice(rolls)
    
    return {
        "id": str(activity_id),
        "process_nr": process_nr,
        "process": process,
        "out_input": "Input" if random.random() > 0.5 else "Output",
        "ska_inga_i_loneperiod": random.random() > 0.3,
        "fas": random.choice(["Förberedelse", "Körning", "Avstämning", "Avslut"]),
        "roll": roll,
        "behov": f"Genomför aktivitet för {process}",
        "effekten_vardet": f"Säkerställa korrekt {process.lower()}",
        "extra_info": None,
        "acceptans": "Godkänd av ansvarig",
        "feature_losning": "Manuell process",
        "priority": random.randint(1, 5),
        "status": random.choice(["active", "active", "active", "draft"]),
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    }


def generate_fellista_error(period_id: str, error_id: int, employees: List[str]) -> Dict:
    """Generate fellista error"""
    error_code = random.choice(list(ERROR_CODES.keys()))
    error_message = ERROR_CODES[error_code]
    
    severity_map = {
        "E": "error",
        "W": "warning",
        "I": "info"
    }
    severity = severity_map[error_code[0]]
    
    anstnr = random.choice(employees)
    
    detected_date = datetime.now() - timedelta(days=random.randint(0, 10))
    
    is_resolved = random.random() > 0.6
    behandlat = random.random() > 0.4
    
    return {
        "id": f"{period_id}_{error_id:03d}",
        "loneperiod_id": period_id,
        "anstnr": anstnr,
        "error_code": error_code,
        "error_message": error_message,
        "severity": severity,
        "detected_at": detected_date.isoformat(),
        "is_resolved": is_resolved,
        "resolved_at": (detected_date + timedelta(days=random.randint(1, 5))).isoformat() if is_resolved else None,
        "behandlat": behandlat,
        "notes": "Åtgärdad" if is_resolved else ("Under utredning" if behandlat else None)
    }


def generate_korningsstatus(period_id: str) -> Dict:
    """Generate körningsstatus for period"""
    
    # Historical periods have completed runs
    period_year = int(period_id[:4])
    period_month = int(period_id[4:])
    period_date = datetime(period_year, period_month, 1)
    
    is_historical = period_date < datetime.now() - timedelta(days=30)
    
    if is_historical:
        provlon_status = "klar"
        slutlon_status = "klar"
        provlon_run = True
        slutlon_run = True
        
        # Generate realistic timestamps
        provlon_start = period_date + timedelta(days=10)
        provlon_complete = provlon_start + timedelta(hours=2)
        slutlon_start = period_date + timedelta(days=20)
        slutlon_complete = slutlon_start + timedelta(hours=3)
    else:
        # Current/future periods
        provlon_status = random.choice(["ej_startad", "startad", "klar"])
        slutlon_status = "ej_startad" if provlon_status != "klar" else random.choice(["ej_startad", "startad"])
        provlon_run = provlon_status == "klar"
        slutlon_run = slutlon_status == "klar"
        
        provlon_start = datetime.now() - timedelta(days=5) if provlon_status in ["startad", "klar"] else None
        provlon_complete = datetime.now() - timedelta(days=3) if provlon_status == "klar" else None
        slutlon_start = datetime.now() - timedelta(days=1) if slutlon_status == "startad" else None
        slutlon_complete = None
    
    return {
        "loneperiod_id": period_id,
        "la_period_code": period_id,
        "provlon_status": provlon_status,
        "provlon_started_at": provlon_start.isoformat() if provlon_start else None,
        "provlon_completed_at": provlon_complete.isoformat() if provlon_complete else None,
        "provlon_run": provlon_run,
        "slutlon_status": slutlon_status,
        "slutlon_started_at": slutlon_start.isoformat() if slutlon_start else None,
        "slutlon_completed_at": slutlon_complete.isoformat() if slutlon_complete else None,
        "slutlon_run": slutlon_run,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    }


# ============================================================================
# SEED FUNCTIONS
# ============================================================================

def seed_employees(count: int = 100):
    """Seed employees"""
    print(f"🌱 Seeding {count} employees...")
    
    batch = db.batch()
    employee_ids = []
    
    for i in range(1, count + 1):
        anstnr = f"{10000 + i}"
        employee_ids.append(anstnr)
        employee = generate_employee(10000 + i)
        
        doc_ref = db.collection('employees').document(anstnr)
        batch.set(doc_ref, employee)
        
        if i % 100 == 0:
            batch.commit()
            batch = db.batch()
            print(f"  ✓ Seeded {i} employees")
    
    batch.commit()
    print(f"✅ Seeded {count} employees")
    return employee_ids


def seed_loneperiods():
    """Seed löneperiods (12 months: 2025-2026)"""
    print("🌱 Seeding löneperiods...")
    
    periods = []
    batch = db.batch()
    
    # 12 months from Jan 2025 to Dec 2025
    for month in range(1, 13):
        period = generate_loneperiod(2025, month)
        periods.append(period)
        
        doc_ref = db.collection('loneperiods').document(period["id"])
        batch.set(doc_ref, period)
    
    batch.commit()
    print(f"✅ Seeded {len(periods)} löneperiods")
    return [p["id"] for p in periods]


def seed_activities(count: int = 50):
    """Seed activities"""
    print(f"🌱 Seeding {count} activities...")
    
    batch = db.batch()
    activity_ids = []
    
    for i in range(1, count + 1):
        activity_id = str(i)
        activity_ids.append(activity_id)
        activity = generate_activity(i)
        
        doc_ref = db.collection('activities').document(activity_id)
        batch.set(doc_ref, activity)
        
        if i % 50 == 0:
            batch.commit()
            batch = db.batch()
            print(f"  ✓ Seeded {i} activities")
    
    batch.commit()
    print(f"✅ Seeded {count} activities")
    return activity_ids


def seed_fellistor(period_ids: List[str], employee_ids: List[str], errors_per_period: int = 10):
    """Seed fellistor"""
    print(f"🌱 Seeding fellistor ({errors_per_period} errors per period)...")
    
    total_errors = 0
    batch = db.batch()
    
    for period_id in period_ids:
        for i in range(1, errors_per_period + 1):
            error = generate_fellista_error(period_id, i, employee_ids)
            
            doc_ref = db.collection('fellistor').document(error["id"])
            batch.set(doc_ref, error)
            total_errors += 1
            
            if total_errors % 100 == 0:
                batch.commit()
                batch = db.batch()
                print(f"  ✓ Seeded {total_errors} errors")
    
    batch.commit()
    print(f"✅ Seeded {total_errors} fellistor entries")


def seed_korningsstatus(period_ids: List[str]):
    """Seed körningsstatus"""
    print("🌱 Seeding körningsstatus...")
    
    batch = db.batch()
    
    for period_id in period_ids:
        korning = generate_korningsstatus(period_id)
        
        doc_ref = db.collection('la_period_mappings').document()
        batch.set(doc_ref, korning)
    
    batch.commit()
    print(f"✅ Seeded {len(period_ids)} körningsstatus entries")


def seed_assignments(period_ids: List[str], activity_ids: List[str], assignments_per_period: int = 20):
    """Seed assignments"""
    print(f"🌱 Seeding assignments ({assignments_per_period} per period)...")
    
    total_assignments = 0
    batch = db.batch()
    
    for period_id in period_ids:
        # Random selection of activities for this period
        selected_activities = random.sample(activity_ids, min(assignments_per_period, len(activity_ids)))
        
        for activity_id in selected_activities:
            assignment = {
                "loneperiod_id": period_id,
                "activity_id": activity_id,
                "is_completed": random.random() > 0.3,  # 70% completed
                "created_at": firestore.SERVER_TIMESTAMP
            }
            
            doc_ref = db.collection('assignments').document()
            batch.set(doc_ref, assignment)
            total_assignments += 1
            
            if total_assignments % 100 == 0:
                batch.commit()
                batch = db.batch()
                print(f"  ✓ Seeded {total_assignments} assignments")
    
    batch.commit()
    print(f"✅ Seeded {total_assignments} assignments")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Seed all test data"""
    print("\n" + "="*70)
    print("🔥 FIRESTORE TEST DATA SEEDER")
    print("="*70 + "\n")
    
    try:
        # Seed in order
        employee_ids = seed_employees(100)
        period_ids = seed_loneperiods()
        activity_ids = seed_activities(50)
        seed_fellistor(period_ids, employee_ids, errors_per_period=10)
        seed_korningsstatus(period_ids)
        seed_assignments(period_ids, activity_ids, assignments_per_period=20)
        
        print("\n" + "="*70)
        print("✅ ALL TEST DATA SEEDED SUCCESSFULLY!")
        print("="*70)
        print(f"\n📊 Summary:")
        print(f"  - Employees: {len(employee_ids)}")
        print(f"  - Löneperiods: {len(period_ids)}")
        print(f"  - Activities: {len(activity_ids)}")
        print(f"  - Fellistor: {len(period_ids) * 10}")
        print(f"  - Körningsstatus: {len(period_ids)}")
        print(f"  - Assignments: ~{len(period_ids) * 20}")
        print(f"\n🔥 Firestore database ready for testing!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
