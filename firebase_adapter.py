#!/usr/bin/env python3
"""
Firebase Firestore Adapter
Converts SQLite-style queries to Firestore operations
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from firebase_admin import firestore
import logging
from config import get_db

logger = logging.getLogger(__name__)


class FirestoreAdapter:
    """Adapter for Firestore database operations"""
    
    def __init__(self):
        # Lazy initialization - get_db() will initialize Firebase if needed
        self._db = None
    
    @property
    def db(self):
        """Lazy-loaded Firestore client"""
        if self._db is None:
            self._db = get_db()
        return self._db
    
    # ========================================================================
    # LONEPERIODS
    # ========================================================================
    
    def get_loneperiods(self, skip: int = 0, limit: int = 100, 
                       status: Optional[str] = None, year: Optional[int] = None) -> List[Dict]:
        """Get löneperioder from Firestore"""
        query = self.db.collection('loneperiods')
        
        if status:
            query = query.where('status', '==', status)
        
        if year:
            # Filter by year in start_date
            query = query.where('year', '==', year)
        
        query = query.limit(limit).offset(skip)
        
        docs = query.stream()
        return [{'id': doc.id, **doc.to_dict()} for doc in docs]
    
    def get_loneperiod(self, period_id: int) -> Optional[Dict]:
        """Get specific löneperiod"""
        doc = self.db.collection('loneperiods').document(str(period_id)).get()
        if doc.exists:
            return {'id': doc.id, **doc.to_dict()}
        return None
    
    def create_loneperiod(self, data: Dict) -> Dict:
        """Create new löneperiod"""
        doc_ref = self.db.collection('loneperiods').document()
        data['created_at'] = firestore.SERVER_TIMESTAMP
        data['updated_at'] = firestore.SERVER_TIMESTAMP
        doc_ref.set(data)
        return {'id': doc_ref.id, **data}
    
    def update_loneperiod(self, period_id: int, data: Dict) -> Optional[Dict]:
        """Update löneperiod"""
        doc_ref = self.db.collection('loneperiods').document(str(period_id))
        if not doc_ref.get().exists:
            return None
        
        data['updated_at'] = firestore.SERVER_TIMESTAMP
        doc_ref.update(data)
        return self.get_loneperiod(period_id)
    
    # ========================================================================
    # ACTIVITIES
    # ========================================================================
    
    def get_activities(self, skip: int = 0, limit: int = 100,
                      process: Optional[str] = None, role: Optional[str] = None,
                      status: Optional[str] = None) -> List[Dict]:
        """Get activities from Firestore"""
        query = self.db.collection('activities')
        
        if process:
            query = query.where('process', '==', process)
        if role:
            query = query.where('roll', '==', role)
        if status:
            query = query.where('status', '==', status)
        
        query = query.limit(limit).offset(skip)
        
        docs = query.stream()
        return [{'id': doc.id, **doc.to_dict()} for doc in docs]
    
    def get_activity(self, activity_id: int) -> Optional[Dict]:
        """Get specific activity"""
        doc = self.db.collection('activities').document(str(activity_id)).get()
        if doc.exists:
            return {'id': doc.id, **doc.to_dict()}
        return None
    
    def create_activity(self, data: Dict) -> Dict:
        """Create new activity"""
        doc_ref = self.db.collection('activities').document()
        data['created_at'] = firestore.SERVER_TIMESTAMP
        data['updated_at'] = firestore.SERVER_TIMESTAMP
        doc_ref.set(data)
        return {'id': doc_ref.id, **data}
    
    def update_activity(self, activity_id: int, data: Dict) -> Optional[Dict]:
        """Update activity"""
        doc_ref = self.db.collection('activities').document(str(activity_id))
        if not doc_ref.get().exists:
            return None
        
        data['updated_at'] = firestore.SERVER_TIMESTAMP
        doc_ref.update(data)
        return self.get_activity(activity_id)
    
    def delete_activity(self, activity_id: int) -> bool:
        """Delete activity"""
        doc_ref = self.db.collection('activities').document(str(activity_id))
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True
    
    # ========================================================================
    # EMPLOYEES
    # ========================================================================
    
    def get_employees(self, org_kod: Optional[str] = None, 
                     status: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Get employees from Firestore"""
        query = self.db.collection('employees')
        
        if org_kod:
            query = query.where('org_kod', '==', org_kod)
        if status:
            query = query.where('status', '==', status)
        
        query = query.limit(limit)
        
        docs = query.stream()
        # Return with 'id' field for Pydantic validation
        results = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id  # Use document ID as id
            results.append(data)
        return results
    
    # ========================================================================
    # FELLISTOR
    # ========================================================================
    
    def get_fellistor(self, loneperiod_id: int, severity: Optional[str] = None,
                     visa_endast_obehandlade: bool = False,
                     visa_endast_olosta: bool = False) -> List[Dict]:
        """Get fellistor from Firestore"""
        query = self.db.collection('fellistor').where('loneperiod_id', '==', str(loneperiod_id))
        
        if severity:
            query = query.where('severity', '==', severity)
        if visa_endast_obehandlade:
            query = query.where('behandlat', '==', False)
        if visa_endast_olosta:
            query = query.where('is_resolved', '==', False)
        
        query = query.order_by('detected_at', direction=firestore.Query.DESCENDING)
        
        docs = query.stream()
        return [{'id': doc.id, **doc.to_dict()} for doc in docs]
    
    def get_fellista_summary(self, loneperiod_id: int) -> Dict:
        """Get fellista summary"""
        all_errors = self.get_fellistor(loneperiod_id)
        
        summary = {
            'loneperiod_id': loneperiod_id,
            'total_errors': 0,
            'total_warnings': 0,
            'total_info': 0,
            'unresolved_errors': 0,
            'unresolved_warnings': 0,
            'obehandlade': 0,
            'errors_by_code': {}
        }
        
        for error in all_errors:
            severity = error.get('severity')
            if severity == 'error':
                summary['total_errors'] += 1
                if not error.get('is_resolved'):
                    summary['unresolved_errors'] += 1
            elif severity == 'warning':
                summary['total_warnings'] += 1
                if not error.get('is_resolved'):
                    summary['unresolved_warnings'] += 1
            elif severity == 'info':
                summary['total_info'] += 1
            
            if not error.get('behandlat'):
                summary['obehandlade'] += 1
            
            error_code = error.get('error_code', 'UNKNOWN')
            summary['errors_by_code'][error_code] = summary['errors_by_code'].get(error_code, 0) + 1
        
        return summary
    
    def update_fellista_error(self, error_id: str, data: Dict) -> Optional[Dict]:
        """Update fellista error"""
        doc_ref = self.db.collection('fellistor').document(error_id)
        if not doc_ref.get().exists:
            return None
        
        if data.get('is_resolved'):
            data['resolved_at'] = firestore.SERVER_TIMESTAMP
        
        doc_ref.update(data)
        
        doc = doc_ref.get()
        return {'id': doc.id, **doc.to_dict()}
    
    # ========================================================================
    # KÖRNINGSSTATUS
    # ========================================================================
    
    def get_korningsstatus(self, loneperiod_id: int) -> Optional[Dict]:
        """Get körningsstatus for löneperiod"""
        # Get from la_period_mappings collection
        query = self.db.collection('la_period_mappings').where('loneperiod_id', '==', str(loneperiod_id))
        docs = list(query.stream())
        
        if not docs:
            return None
        
        data = docs[0].to_dict()
        
        # Calculate can_start flags
        provlon_status = data.get('provlon_status', 'ej_startad')
        slutlon_status = data.get('slutlon_status', 'ej_startad')
        
        can_start_provlon = provlon_status in ['ej_startad', 'fel']
        can_start_slutlon = (provlon_status == 'klar' and slutlon_status in ['ej_startad', 'fel'])
        
        return {
            'loneperiod_id': loneperiod_id,
            'la_period_code': data.get('la_period_code', ''),
            'provlon_status': provlon_status,
            'provlon_started_at': data.get('provlon_started_at'),
            'provlon_completed_at': data.get('provlon_completed_at'),
            'slutlon_status': slutlon_status,
            'slutlon_started_at': data.get('slutlon_started_at'),
            'slutlon_completed_at': data.get('slutlon_completed_at'),
            'can_start_provlon': can_start_provlon,
            'can_start_slutlon': can_start_slutlon
        }
    
    def update_korningsstatus(self, loneperiod_id: int, data: Dict) -> Optional[Dict]:
        """Update körningsstatus"""
        query = self.db.collection('la_period_mappings').where('loneperiod_id', '==', str(loneperiod_id))
        docs = list(query.stream())
        
        if not docs:
            return None
        
        doc_ref = docs[0].reference
        
        # Handle status transitions
        now = firestore.SERVER_TIMESTAMP
        
        if 'provlon_status' in data:
            if data['provlon_status'] == 'startad':
                data['provlon_started_at'] = now
            elif data['provlon_status'] in ['klar', 'fel']:
                data['provlon_completed_at'] = now
                data['provlon_run'] = True
        
        if 'slutlon_status' in data:
            if data['slutlon_status'] == 'startad':
                data['slutlon_started_at'] = now
            elif data['slutlon_status'] in ['klar', 'fel']:
                data['slutlon_completed_at'] = now
                data['slutlon_run'] = True
        
        doc_ref.update(data)
        
        return self.get_korningsstatus(loneperiod_id)
    
    # ========================================================================
    # ASSIGNMENTS
    # ========================================================================
    
    def get_loneperiod_progress(self, loneperiod_id: int) -> Dict:
        """Get progress for löneperiod"""
        query = self.db.collection('assignments').where('loneperiod_id', '==', str(loneperiod_id))
        all_assignments = list(query.stream())
        
        total = len(all_assignments)
        completed = sum(1 for a in all_assignments if a.to_dict().get('is_completed'))
        
        return {
            'loneperiod_id': loneperiod_id,
            'completion_percentage': round((completed / total * 100) if total > 0 else 0.0, 2),
            'completed_count': completed,
            'total_count': total,
            'pending_count': total - completed
        }
    
    def add_activities_to_loneperiod(self, loneperiod_id: int, activity_ids: List[int]) -> int:
        """Add activities to löneperiod"""
        added = 0
        
        for activity_id in activity_ids:
            # Check if assignment already exists
            query = self.db.collection('assignments') \
                .where('loneperiod_id', '==', str(loneperiod_id)) \
                .where('activity_id', '==', str(activity_id))
            
            if not list(query.stream()):
                # Create new assignment
                self.db.collection('assignments').add({
                    'loneperiod_id': str(loneperiod_id),
                    'activity_id': str(activity_id),
                    'is_completed': False,
                    'created_at': firestore.SERVER_TIMESTAMP
                })
                added += 1
        
        return added
