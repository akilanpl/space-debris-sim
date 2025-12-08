from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class MissionConfig:
    commander: str
    rocket_name: str
    orbit_range_km: float
    launch_lat: float
    launch_lon: float
    country: str
    space_station: str

@dataclass
class DebrisItem:
    material: str
    mass_kg: float

@dataclass
class Thruster:
    id: int
    speed_history: List[float] = field(default_factory=list)
    debris_collected: List[DebrisItem] = field(default_factory=list)

    def total_mass(self) -> float:
        return sum(d.mass_kg for d in self.debris_collected)

    def material_breakdown(self) -> Dict[str, float]:
        out = {}
        for d in self.debris_collected:
            out[d.material] = out.get(d.material, 0.0) + d.mass_kg
        return out
