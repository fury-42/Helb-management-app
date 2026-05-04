from .service import EmergencyService
from .repository import EmergencyRepository
from app.apps.semester.repository import SemesterRepository

def get_emergency_service():
    return EmergencyService(EmergencyRepository(), SemesterRepository())
