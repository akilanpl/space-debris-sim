# Space Debris Simulation — Modular Thruster Framework

Educational research simulation of a modular rocket that deploys three solar-powered thrusters
for orbital debris collection. Provides GUI telemetry, mission logging, debris collection modeling,
and simple data export for research.

## Features
- Login & registration (in-memory for demo)
- Mission config window (orbit altitude, launch site, etc.)
- Main GUI telemetry: temperature, thruster speed, mission log (real-time)
- Simulation phases: prelaunch → ascent → collection → return
- Debris stochastic model with per-thruster collections
- CSV export of telemetry and debris logs
- Simplified orbital helper functions (placeholders for more accurate physics)
- Tests for core modules

## Run locally
```bash
python -m pip install -r requirements.txt
python -m src.space_debris_sim
