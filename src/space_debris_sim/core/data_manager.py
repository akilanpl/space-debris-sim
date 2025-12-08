import csv
import os
import time
from typing import Any
from .models import Thruster
from .simulation import Simulation

class DataManager:
    """Export telemetry and debris logs for offline analysis."""

    def __init__(self, out_dir="exports"):
        self.out_dir = out_dir
        os.makedirs(out_dir, exist_ok=True)

    def export_session(self, sim: Simulation) -> str:
        """Export telemetry CSV and debris CSV. Returns base filename (path)."""
        base = time.strftime("session_%Y%m%d_%H%M%S")
        telem_file = os.path.join(self.out_dir, f"{base}_telemetry.csv")
        debris_file = os.path.join(self.out_dir, f"{base}_debris.csv")

        # Telemetry: time, temperature, avg_speed
        with open(telem_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["time_step", "temperature_C", "avg_speed_m_s"])
            for t, temp, spd in zip(sim.time_axis, sim.temperature_values, sim.avg_speed_values):
                writer.writerow([t, temp, spd])

        # Debris list
        with open(debris_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["thruster_id", "material", "mass_kg"])
            for thr in sim.thrusters:
                for d in thr.debris_collected:
                    writer.writerow([thr.id, d.material, d.mass_kg])

        return telem_file  # return telemetry path as representative
