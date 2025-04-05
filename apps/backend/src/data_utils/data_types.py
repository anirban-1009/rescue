"""Module Containing the Models of the application"""

from dataclasses import dataclass
from typing import List

from src.emergency_centres.model import EmergencyCentre


@dataclass
class GetEmergencyCentreNearMeResponse:
    centres: List[EmergencyCentre]
