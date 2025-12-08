"""
Simulation core. Keeps state and performs discrete time steps.
The design separates logic from UI: UI passes a `log_callback` for messages.
"""

import random
from typing import List, Callable
from .models import Thruster, DebrisItem
from .orbital import estimate_orbital_velocity

class Simulation:
    def __init__(self, config, log_callback: Callable[[str], None]=print):
        self.config = config
        self.log = log_callback
        self.time_step = 0
        self.time_axis = []
        self.temperature_values = []
        self.avg_speed_values = []
        self.thrusters: List[Thruster] = [Thruster(id=i+1) for i in range(3)]
        self.phase = "prelaunch"
        self.thrusters_deployed = False
        self.collection_done = False

    def reset(self):
        self.time_step = 0
        self.time_axis.clear()
        self.temperature_values.clear()
        self.avg_speed_values.clear()
        for t in self.thrusters:
            t.speed_history.clear()
            t.debris_collected.clear()
        self.phase = "ascent"
        self.thrusters_deployed = False
        self.collection_done = False
        self.log("Simulation reset and ascent initiated.")

    def step(self):
        """Execute one time step of simulation."""
        self.time_step += 1
        self.time_axis.append(self.time_step)

        # Temperature modeling (simplified)
        if self.phase == "ascent":
            temp = random.uniform(200, 500)
        elif self.phase == "collection":
            temp = random.uniform(120, 260)
        else:
            temp = random.uniform(80, 200)
        self.temperature_values.append(temp)

        # Thruster speeds (approx orbital velocities)
        speeds = []
        for thr in self.thrusters:
            if self.phase == "ascent":
                speed = random.uniform(4000, 7600)
            elif self.phase == "collection":
                # estimate target orbital speed from orbit altitude
                vel = estimate_orbital_velocity(self.config.orbit_range_km)
                speed = random.uniform(vel - 50, vel + 50)
            else:
                speed = random.uniform(3000, 7000)
            thr.speed_history.append(speed)
            speeds.append(speed)
        avg_speed = sum(speeds) / len(speeds)
        self.avg_speed_values.append(avg_speed)

        # Phase transitions
        if self.phase == "ascent" and self.time_step >= 10:
            self._deploy_thrusters()
        if self.phase == "collection" and self.time_step >= 25:
            self._finish_collection()

        # Collection steps
        if self.phase == "collection" and self.thrusters_deployed:
            self._collect_debris_step()

    def _deploy_thrusters(self):
        if self.thrusters_deployed:
            return
        self.thrusters_deployed = True
        self.phase = "collection"
        self.log("Thrusters deployed into independent orbits for collection.")

    def _finish_collection(self):
        if self.collection_done:
            return
        self.collection_done = True
        self.phase = "return"
        self.log("Collection window closed. Preparing return / disposal.")

    def _collect_debris_step(self):
        materials = ["metal", "plastic", "electronics", "organic"]
        weights = [0.5, 0.2, 0.2, 0.1]
        for thr in self.thrusters:
            if random.random() < 0.6:
                mat = random.choices(materials, weights=weights, k=1)[0]
                mass = round(random.uniform(5.0, 40.0), 1)
                debris = DebrisItem(material=mat, mass_kg=mass)
                thr.debris_collected.append(debris)
                self.log(f"Thruster {thr.id} captured {mass:.1f} kg of {mat}.")