"""
Pydantic models for Löneprocess API v3.0
All request/response schemas - FIXED FOR FIRESTORE
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class EmployeeStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    terminated = "terminated"


class PeriodStatus(str, Enum):
    planned = "planned"
    active = "active"
    upcoming = "upcoming"
    completed = "completed"
    provlon = "provlon"
    slutlon = "slutlon"
    closed = "closed"


class AbsenceType(str, Enum):
    sjuk = "sjuk"
    semester = "semester"
    vab = "vab"
    foraldraledig = "foraldraledig"
    annan = "annan"


class ErrorSeverity(str, Enum):
    error = "error"
    warning = "warning"
    info = "info"


class KorningsStatus(str, Enum):
    ej_startad = "ej_startad"
    startad = "startad"
    pagar = "pagar"
    klar = "klar"
    fel = "fel"


class SyncStatus(str, Enum):
    success = "success"
    failed = "failed"
    partial = "partial"


# ============================================================================
# ACTIVITIES MODELS - FIXED FOR FIRESTORE
# ============================================================================

class ActivityBase(BaseModel):
    process_nr: Optional[str] = Field(None, max_length=50)
    process: Optional[str] = Field(None, max_length=200)
    out_input: Optional[str] = Field(None, max_length=500)
    ska_inga_i_loneperiod: bool = False
    fas: Optional[str] = None  # FIXED: Changed from int to str ("Förberedelse", "Körning", etc)
    roll: Optional[str] = Field(None, max_length=100)
    behov: Optional[str] = None
    effekten_vardet: Optional[str] = None
    extra_info: Optional[str] = None
    acceptans: Optional[str] = None
    feature_losning: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = Field("active", pattern="^(active|draft|pending|in_progress|completed|blocked)$")  # FIXED: Added active/draft


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    process_nr: Optional[str] = None
    process: Optional[str] = None
    out_input: Optional[str] = None
    ska_inga_i_loneperiod: Optional[bool] = None
    fas: Optional[str] = None  # FIXED
    roll: Optional[str] = None
    behov: Optional[str] = None
    effekten_vardet: Optional[str] = None
    extra_info: Optional[str] = None
    acceptans: Optional[str] = None
    feature_losning: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = None


class ActivityResponse(ActivityBase):
    id: str  # FIXED: Changed from int to str
    created_at: Any  # FIXED: Allow Firestore Timestamp
    updated_at: Optional[Any] = None  # FIXED: Allow Firestore Timestamp


# ============================================================================
# LONEPERIODS MODELS
# ============================================================================

class LoneperiodBase(BaseModel):
    name: str = Field(..., max_length=100)
    start_date: str  # FIXED: Changed from date to str
    end_date: str  # FIXED: Changed from date to str
    status: str = Field("planned", pattern="^(planned|active|upcoming|completed|provlon|slutlon|closed)$")


class LoneperiodCreate(LoneperiodBase):
    pass


class LoneperiodUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[str] = None  # FIXED
    end_date: Optional[str] = None  # FIXED
    status: Optional[str] = None
    completion_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)


class LoneperiodResponse(LoneperiodBase):
    id: str  # FIXED
    year: Optional[int] = None
    month: Optional[int] = None
    completion_percentage: Optional[float] = None
    created_at: Optional[Any] = None  # FIXED
    updated_at: Optional[Any] = None  # FIXED


class LoneperiodProgressResponse(BaseModel):
    loneperiod_id: int
    completion_percentage: float
    completed_count: int
    total_count: int
    pending_count: int


class AddActivitiesRequest(BaseModel):
    activity_ids: List[int] = Field(..., min_length=1)


# ============================================================================
# LA EMPLOYEES MODELS
# ============================================================================

class LAEmployeeBase(BaseModel):
    anstnr: str
    fnamn: Optional[str] = None
    enamn: Optional[str] = None
    personnummer: Optional[str] = None
    org_kod: Optional[str] = None
    org_namn: Optional[str] = None
    bef_kod: Optional[str] = None
    bef_namn: Optional[str] = None
    arbl: Optional[str] = None
    anstdat: Optional[str] = None
    avgdat: Optional[str] = None
    status: str = "active"  # FIXED: Removed EmployeeStatus enum
    heltidslon: Optional[float] = None
    syssgrad: Optional[float] = None


class LAEmployeeResponse(LAEmployeeBase):
    id: str  # FIXED
    last_synced_at: Optional[Any] = None  # FIXED
    created_at: Optional[Any] = None  # FIXED


# ============================================================================
# LA ABSENCES MODELS
# ============================================================================

class LAAbsenceBase(BaseModel):
    anstnr: str
    absence_code: Optional[str] = None
    absence_type: Optional[str] = None  # FIXED: Removed enum
    absence_description: Optional[str] = None
    start_date: str
    end_date: str
    hours: Optional[float] = None
    days: Optional[float] = None
    loneperiod_id: Optional[int] = None


class LAAbsenceResponse(LAAbsenceBase):
    id: int
    last_synced_at: Optional[str] = None
    created_at: str


# ============================================================================
# LA VACATION MODELS
# ============================================================================

class LAVacationBalance(BaseModel):
    anstnr: str
    semratt: Optional[float] = None
    semspar: Optional[float] = None
    uttagna: Optional[float] = None
    kvar: Optional[float] = None
    semlongr: Optional[float] = None
    as_of_date: str


# ============================================================================
# LA BENEFITS MODELS
# ============================================================================

class LABenefitBase(BaseModel):
    anstnr: str
    benefit_type: str
    benefit_code: Optional[str] = None
    benefit_value: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class LABenefitResponse(LABenefitBase):
    id: int
    last_synced_at: Optional[str] = None
    created_at: str


# ============================================================================
# LA TAX MODELS
# ============================================================================

class LATaxInfo(BaseModel):
    anstnr: str
    skattetabell: Optional[str] = None
    skattekod: Optional[str] = None
    avdragskod_1: Optional[str] = None
    avdragskod_2: Optional[str] = None
    avdragskod_3: Optional[str] = None
    fackavgift_mottagare: Optional[str] = None
    fackavgift_procent: Optional[float] = None


# ============================================================================
# v3.0 FELLISTOR MODELS
# ============================================================================

class LACalculationErrorBase(BaseModel):
    loneperiod_id: Optional[str] = None  # FIXED
    anstnr: Optional[str] = None
    error_code: str
    error_message: str
    field_name: Optional[str] = None
    severity: str  # FIXED: Removed enum
    behandlat: bool = False
    notes: Optional[str] = None


class LACalculationErrorResponse(LACalculationErrorBase):
    id: str  # FIXED
    is_resolved: bool
    detected_at: str
    resolved_at: Optional[str] = None


class LACalculationErrorCreate(LACalculationErrorBase):
    pass


class LACalculationErrorUpdate(BaseModel):
    behandlat: Optional[bool] = None
    is_resolved: Optional[bool] = None
    notes: Optional[str] = None


class FellistaSummary(BaseModel):
    loneperiod_id: int
    total_errors: int
    total_warnings: int
    total_info: int
    unresolved_errors: int
    unresolved_warnings: int
    obehandlade: int
    errors_by_code: Dict[str, int]


# ============================================================================
# v3.0 KÖRNINGSSTATUS MODELS
# ============================================================================

class KorningsStatusResponse(BaseModel):
    loneperiod_id: int
    la_period_code: str
    provlon_status: str
    provlon_started_at: Optional[str] = None
    provlon_completed_at: Optional[str] = None
    slutlon_status: str
    slutlon_started_at: Optional[str] = None
    slutlon_completed_at: Optional[str] = None
    can_start_provlon: bool
    can_start_slutlon: bool


class KorningsStatusUpdate(BaseModel):
    provlon_status: Optional[str] = None
    slutlon_status: Optional[str] = None


# ============================================================================
# SYNC MODELS
# ============================================================================

class SyncResponse(BaseModel):
    status: str
    sync_type: str
    records_synced: int
    timestamp: str
    message: Optional[str] = None


class LASyncLogEntry(BaseModel):
    id: int
    sync_type: str
    status: str  # FIXED: Removed enum
    records_synced: int
    error_message: Optional[str] = None
    started_at: str
    completed_at: Optional[str] = None
