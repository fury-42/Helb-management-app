from .service import SemesterService
from .repository import SemesterRepository

def get_semester_service():
    return SemesterService(SemesterRepository())
