from src.models.emergency_centres import EmergencyCentre
from typing import List
from dataclasses import dataclass


@dataclass
class GetEmergencyCentreNearMeResponse:
    centres: List[EmergencyCentre]
